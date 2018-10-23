from hypothesis import given
from hypothesis import strategies as st

from functoolsplus.collections import SingleLinkedList


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
