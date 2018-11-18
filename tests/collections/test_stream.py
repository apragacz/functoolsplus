import pytest
from hypothesis import given
from hypothesis import strategies as st

from functoolsplus import filter as generic_filter
from functoolsplus import flatmap
from functoolsplus import map as generic_map
from functoolsplus import unit
from functoolsplus.collections import Stream
from tests import strategies as tests_st


def test_empty_stream_is_a_singleton():
    assert Stream() is Stream.empty
    assert Stream([]) is Stream.empty


@given(st.integers(), st.lists(st.integers()))
def test_cons(input_value, input_list):
    stream = Stream.cons(input_value, lambda: Stream([input_list]))
    assert stream[0] == input_value


def test_cons_invalid():
    with pytest.raises(TypeError):
        Stream.cons(1, 2)


def test_cons_invalid_lazy_evaluator():
    stream = Stream.cons(1, lambda: 2)
    with pytest.raises(AttributeError):
        stream.tail


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_concat(input_list1, input_list2):
    s1 = Stream(input_list1)
    s2 = Stream(input_list2)
    assert list(s1 + s2) == input_list1 + input_list2


@given(st.lists(st.integers()), st.text())
def test_concat_with_str(input_list, input_str):
    with pytest.raises(TypeError):
        Stream(input_list) + input_str


@given(st.lists(st.integers()))
def test_isinstance(input_list):
    lst = Stream(input_list)
    assert isinstance(lst, Stream)


@given(st.lists(st.integers()), tests_st.integer_functions())
def test_map(input_list, func):
    stream = Stream(input_list)
    assert isinstance(generic_map(func, stream), Stream)
    assert list(generic_map(func, stream)) == [func(x) for x in input_list]


@given(st.lists(st.integers()), tests_st.integer_predicates())
def test_filter(input_list, pred):
    stream = Stream(input_list)
    expected_list = [x for x in input_list if pred(x)]
    assert isinstance(generic_filter(pred, stream), Stream)
    assert list(generic_filter(pred, stream)) == expected_list


@given(st.lists(st.integers()), tests_st.integer_expand_functions(Stream))
def test_flatmap(input_list, expand_func):
    stream = Stream(input_list)
    expected_list = [y for x in input_list for y in expand_func(x)]
    assert isinstance(flatmap(expand_func, stream), Stream)
    assert list(flatmap(expand_func, stream)) == expected_list


@given(st.integers())
def test_unit(n):
    stream = unit(Stream, n)
    assert isinstance(stream, Stream)
    assert stream.head == n
    assert stream.tail == Stream.empty


@given(st.lists(st.integers()), st.integers())
def test_getitem_int_key(input_list, i):
    n = len(input_list)
    stream = Stream(input_list)
    if 0 <= i < n:
        assert stream[i] == input_list[i]
    else:
        with pytest.raises(IndexError):
            stream[i]


@given(st.lists(st.integers()), st.text())
def test_getitem_str_key(input_list, key):
    stream = Stream(input_list)
    with pytest.raises(TypeError):
        stream[key]


@given(st.lists(st.integers()))
def test_str(input_list):
    stream = Stream(input_list)
    assert 'Stream' in str(stream)
    for elem in input_list:
        assert repr(elem) in str(stream)


def test_unevaluated_str():
    stream = Stream.cons(1, lambda: Stream([2]))
    assert str(stream) == 'Stream([1, <unevaluated>])'
    assert stream[1] == 2
    assert str(stream) == 'Stream([1, 2])'


def test_empty_head():
    with pytest.raises(AttributeError):
        Stream.empty.head


def test_empty_tail():
    with pytest.raises(AttributeError):
        Stream.empty.tail
