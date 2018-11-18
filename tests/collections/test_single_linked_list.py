import pytest
from hypothesis import given
from hypothesis import strategies as st

from functoolsplus import filter as generic_filter
from functoolsplus import flatmap
from functoolsplus import map as generic_map
from functoolsplus import unit
from functoolsplus.collections import SingleLinkedList
from tests import strategies as tests_st


def test_empty_list_is_a_singleton():
    assert SingleLinkedList() is SingleLinkedList.empty
    assert SingleLinkedList([]) is SingleLinkedList.empty


@given(st.lists(st.integers()))
def test_len(input_list):
    lst = SingleLinkedList(input_list)
    assert len(lst) == len(input_list)


@given(st.lists(st.integers()))
def test_eq(input_list):
    lst1 = SingleLinkedList(input_list)
    lst2 = SingleLinkedList(input_list)
    assert lst1 == lst2


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_neq(input_list1, input_list2):
    if input_list1 == input_list2:
        return
    lst1 = SingleLinkedList(input_list1)
    lst2 = SingleLinkedList(input_list2)
    assert lst1 != lst2


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_concat(input_list1, input_list2):
    lst1 = SingleLinkedList(input_list1)
    lst2 = SingleLinkedList(input_list2)
    assert lst1 + lst2 == SingleLinkedList(input_list1 + input_list2)


@given(st.lists(st.integers()), st.lists(st.integers()))
def test_concat_list(input_list1, input_list2):
    lst1 = SingleLinkedList(input_list1)
    with pytest.raises(TypeError):
        lst1 + input_list2


@given(st.lists(st.integers()))
def test_isinstance(input_list):
    lst = SingleLinkedList(input_list)
    assert isinstance(lst, SingleLinkedList)


@given(st.lists(st.integers()))
def test_reversed(input_list):
    lst = SingleLinkedList(input_list)
    reversed_lst = lst.reversed()
    assert len(lst) == len(reversed_lst)
    assert len(lst) > 1 or lst == reversed_lst
    assert reversed_lst.reversed() == lst


@given(st.lists(st.integers()), st.integers())
def test_appended_left(input_list, value):
    lst = SingleLinkedList(input_list)
    assert lst.appended_left(value) == SingleLinkedList([value] + input_list)
    assert lst == SingleLinkedList(input_list)


@given(st.lists(st.integers(), min_size=1))
def test_popped_left_nonempty(input_list):
    lst = SingleLinkedList(input_list)
    assert lst.popped_left() == SingleLinkedList(input_list[1:])
    assert lst == SingleLinkedList(input_list)


def test_popped_left_empty():
    lst = SingleLinkedList()
    with pytest.raises(ValueError):
        lst.popped_left()


@given(st.lists(st.integers()), tests_st.integer_functions())
def test_map(input_list, func):
    lst = SingleLinkedList(input_list)
    expected_lst = SingleLinkedList(func(x) for x in input_list)
    assert generic_map(func, lst) == expected_lst


@given(st.lists(st.integers()), tests_st.integer_predicates())
def test_filter(input_list, pred):
    lst = SingleLinkedList(input_list)
    expected_lst = SingleLinkedList(x for x in input_list if pred(x))
    assert generic_filter(pred, lst) == expected_lst


@given(
    st.lists(st.integers()),
    tests_st.integer_expand_functions(SingleLinkedList))
def test_flatmap(input_list, expand_func):
    lst = SingleLinkedList(input_list)
    expected_list = [y for x in input_list for y in expand_func(x)]
    assert isinstance(flatmap(expand_func, lst), SingleLinkedList)
    assert list(flatmap(expand_func, lst)) == expected_list


@given(st.integers())
def test_unit(n):
    lst = unit(SingleLinkedList, n)
    assert lst == SingleLinkedList([n])


@given(st.lists(st.integers()), st.integers())
def test_getitem_int_key(input_list, i):
    n = len(input_list)
    lst = SingleLinkedList(input_list)
    if 0 <= i < n:
        assert lst[i] == input_list[i]
    else:
        with pytest.raises(IndexError):
            lst[i]


@given(st.lists(st.integers()), st.text())
def test_getitem_str_key(input_list, key):
    lst = SingleLinkedList(input_list)
    with pytest.raises(TypeError):
        lst[key]


@given(st.lists(st.integers()))
def test_str(input_list):
    stream = SingleLinkedList(input_list)
    assert 'SingleLinkedList' in str(stream)
    for elem in input_list:
        assert repr(elem) in str(stream)


def test_empty_head():
    with pytest.raises(AttributeError):
        SingleLinkedList.empty.head


def test_empty_tail():
    with pytest.raises(AttributeError):
        SingleLinkedList.empty.tail
