import pytest
from hypothesis import given
from hypothesis import strategies as st

from functoolsplus import filter as generic_filter
from functoolsplus import flatmap, fold
from functoolsplus import map as generic_map
from functoolsplus import unit
from functoolsplus.abc import Filterable, Foldable, Functor, Monad
from functoolsplus.utils.singletons import Missing
from tests import strategies as tests_st
from tests.functions import add, always_false, identity


class FallbackImpl(Filterable, Foldable, Functor, Monad, object):

    def __init__(self, value):
        self._value = value

    def __fold__(self, func, *, initial_value=Missing):
        return super().__fold__(func, initial_value=initial_value)

    def __filter__(self, func):
        return super().__filter__(func)

    def __map__(self, func):
        return super().__map__(func)

    def __flatmap__(self, func):
        return super().__flatmap__(func)

    @staticmethod
    def __unit__(cls, value):
        return super().__unit__(cls, value)


class NoImpl(Filterable, Foldable, Functor, Monad, object):

    def __init__(self, value):
        self._value = value

    __fold__ = None
    __filter__ = None
    __map__ = None
    __flatmap__ = None
    __unit__ = None


@given(st.lists(st.integers()), tests_st.integer_functions())
def test_list_map(input_list, func):
    assert generic_map(func, input_list) == [func(x) for x in input_list]


@given(st.lists(st.integers()), tests_st.integer_predicates())
def test_list_filter(input_list, pred):
    assert generic_filter(pred, input_list) == [
        x for x in input_list if pred(x)]


@given(st.lists(st.integers(), min_size=1))
def test_list_fold_sum(input_list):
    assert fold(lambda x, y: x + y, input_list) == sum(input_list)


def test_list_fold_sum_on_empty():
    with pytest.raises(ValueError):
        fold(lambda x, y: x + y, [])


@given(st.lists(st.integers()))
def test_list_fold_sum_with_initial_value(input_list):
    assert fold(
        lambda x, y: x + y, input_list, initial_value=0) == sum(input_list)


@given(st.lists(st.integers()), tests_st.integer_expand_functions(list))
def test_list_flatmap(input_list, expand_func):
    assert flatmap(expand_func, input_list) == [
        y for x in input_list for y in expand_func(x)]


@given(st.integers())
def test_list_unit(n):
    assert unit(list, n) == [n]


@given(st.integers(), tests_st.integer_functions())
def test_int_map(n, func):
    with pytest.raises(TypeError):
        generic_map(func, n)


@given(st.integers())
def test_int_filter(n):
    with pytest.raises(TypeError):
        generic_filter(always_false, n)


@given(st.integers())
def test_int_fold(n):
    with pytest.raises(TypeError):
        fold(identity, n)


@given(st.integers())
def test_int_flatmap(n):
    with pytest.raises(TypeError):
        flatmap(identity, n)


@given(st.integers())
def test_int_unit(n):
    with pytest.raises(TypeError):
        unit(int, n)


def test_fallback_impl_map():
    with pytest.raises(TypeError):
        generic_map(identity, FallbackImpl(42))


def test_fallback_impl_filter():
    with pytest.raises(TypeError):
        generic_filter(always_false, FallbackImpl(42))


def test_fallback_impl_fold():
    with pytest.raises(TypeError):
        fold(add, FallbackImpl(42))


def test_fallback_impl_flatmap():
    with pytest.raises(TypeError):
        flatmap(lambda x: FallbackImpl(x), FallbackImpl(42))


def test_fallback_impl_unit():
    with pytest.raises(TypeError):
        unit(FallbackImpl, 42)


def test_no_impl_map():
    with pytest.raises(TypeError):
        generic_map(identity, NoImpl(42))


def test_no_impl_filter():
    with pytest.raises(TypeError):
        generic_filter(always_false, NoImpl(42))


def test_no_impl_fold():
    with pytest.raises(TypeError):
        fold(add, NoImpl(42))


def test_no_impl_flatmap():
    with pytest.raises(TypeError):
        flatmap(lambda x: NoImpl(x), NoImpl(42))


def test_no_impl_unit():
    with pytest.raises(TypeError):
        unit(NoImpl, 42)
