from collections.abc import Sequence

from functoolsplus.collections.base import SingleLinkedStruct
from functoolsplus.utils.singletons import new_singleton


class SingleLinkedList(SingleLinkedStruct, Sequence):

    def __new__(cls, iterable=None):
        if iterable is None:
            iterable = []
        return cls.from_iterable(iterable)

    @classmethod
    def get_empty(cls):
        return _SingleLinkedListEmptyType()

    @classmethod
    def cons(cls, head, tail):
        return _SingleLinkedListConsType(head, tail)

    @classmethod
    def cons_simple(cls, head, tail):
        return cls.cons(head, tail)

    def __len__(self):
        counter = 0
        lst = self
        while lst:
            lst = lst.tail
            counter += 1
        return counter

    def __eq__(self, other):
        if not isinstance(other, SingleLinkedList):
            return NotImplemented

        lst1 = self
        lst2 = other

        while lst1 and lst2:
            if lst1.head != lst2.head:
                return False

            lst1 = lst1.tail
            lst2 = lst2.tail

        return (not bool(lst1)) and (not bool(lst2))

    def __add__(self, other):
        if not isinstance(other, SingleLinkedList):
            return NotImplemented
        result = other
        for item in reversed(self):
            result = self.cons(item, result)
        return result

    def __map__(self, func):
        result = self.get_empty()
        for item in reversed(self):
            result = self.cons(func(item), result)
        return result

    def __filter__(self, func):
        result = self.get_empty()
        for item in reversed(self):
            if func(item):
                result = self.cons(item, result)
        return result

    def __flatmap__(self, func):
        reversed_result = self.get_empty()
        for item in self:
            for result_item in func(item):
                reversed_result = self.cons(result_item, reversed_result)
        return reversed_result.reversed()

    def __reversed__(self):
        return iter(self.reversed())

    def reversed(self):
        reversed_list = self.get_empty()
        lst = self
        while lst:
            reversed_list = self.cons(lst.head, reversed_list)
            lst = lst.tail
        return reversed_list

    def appended_left(self, item):
        return self.cons(item, self)

    def popped_left(self):
        if not self:
            raise ValueError(f"{type(self).__name__!r} object is empty")
        return self.tail

    def _get_repr_items(self):
        items = []
        lst = self
        while lst:
            items.append(lst.head)
            lst = lst.tail
        return items


class _SingleLinkedListEmptyType(SingleLinkedList):

    def __new__(cls):
        return new_singleton(cls)

    def __bool__(self):
        return False


class _SingleLinkedListConsType(SingleLinkedList):

    def __new__(cls, head, tail):
        obj = object.__new__(cls)
        obj._head = head
        obj._tail = tail
        return obj

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        return self._tail

    def __bool__(self):
        return True


SingleLinkedList.empty = SingleLinkedList.get_empty()

for cls in (
        _SingleLinkedListEmptyType,
        _SingleLinkedListConsType):
    cls.__internal_name__ = cls.__name__
    cls.__name__ = SingleLinkedList.__name__
    cls.__qualname__ = SingleLinkedList.__qualname__
