from functools import partial

from functoolsplus.collections.base import SingleLinkedStruct
from functoolsplus.containers.lazy import LazyValue
from functoolsplus.hof import map as generic_map
from functoolsplus.utils.singletons import new_singleton


class Stream(SingleLinkedStruct):

    def __new__(cls, iterable=None):
        if iterable is None:
            iterable = []
        return cls.from_iterable(iterable)

    @classmethod
    def get_empty(cls):
        return _StreamEmptyType()

    @classmethod
    def cons(cls, head, tail):
        if not isinstance(tail, LazyValue) and callable(tail):
            tail = LazyValue(tail)
        return _StreamConsType(head, tail)

    @classmethod
    def cons_simple(cls, head, tail):
        return cls.cons(head, LazyValue(value=tail))

    def __map__(self, func):
        raise NotImplementedError()

    def _get_repr_items(self):
        items = []
        stream = self
        while stream:
            items.append(stream.head)
            lazy_tail = stream._tail  # pylint: disable=E1101
            if not lazy_tail.is_evaluated():
                items.append(lazy_tail.raw_value)
                break
            stream = stream.tail
        return items


class _StreamEmptyType(Stream):

    def __new__(cls):
        return new_singleton(cls)

    def __bool__(self):
        return False

    def __map__(self, func):
        return self.get_empty()


class _StreamConsType(Stream):

    def __new__(cls, head, tail):
        if not isinstance(tail, LazyValue):
            raise TypeError("'tail' should be lazy value")
        obj = object.__new__(cls)
        obj._head = head
        obj._tail = tail
        return obj

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        value = self._tail.value
        assert isinstance(value, Stream)
        return value

    def __bool__(self):
        return True

    def __map__(self, func):
        return self.cons(
            func(self._head),
            generic_map(partial(generic_map, func), self._tail))


Stream.empty = Stream.get_empty()

for cls in (_StreamEmptyType, _StreamConsType):
    cls.__internal_name__ = cls.__name__
    cls.__name__ = Stream.__name__
    cls.__qualname__ = Stream.__qualname__
