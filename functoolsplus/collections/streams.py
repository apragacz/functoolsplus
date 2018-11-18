from functools import partial

from functoolsplus.collections.base import SingleLinkedStruct
from functoolsplus.containers.lazy import LazyValue
from functoolsplus.hof import filter as generic_filter
from functoolsplus.hof import flatmap
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

    def __add__(self, other):
        if not isinstance(other, Stream):
            return NotImplemented
        return self._appended_with_lazy(LazyValue(value=other))

    def __map__(self, func):
        if not self:
            return self.get_empty()
        return self.cons(
            func(self.head),
            self._map_tail_lazy(partial(generic_map, func)))

    def __filter__(self, func):
        stream = self
        while stream and not func(stream.head):
            stream = stream.tail
        if not stream:
            return self.get_empty()
        return self.cons(
            stream.head,
            stream._map_tail_lazy(partial(generic_filter, func)))

    def __flatmap__(self, func):
        if not self:
            return self.get_empty()
        result_items = func(self.head)
        return result_items._appended_with_lazy(
            self._map_tail_lazy(partial(flatmap, func)))

    def _appended_with_lazy(self, other_stream_lazy):
        if not self:
            return other_stream_lazy.value

        return self.cons(
            self.head,
            self._map_tail_lazy(
                lambda s: s._appended_with_lazy(other_stream_lazy)))

    def _map_tail_lazy(self, func):
        raise NotImplementedError()

    def _get_repr_items(self):
        items = []
        stream = self
        while stream:
            items.append(stream.head)
            lazy_tail = stream._tail_lazy  # pylint: disable=E1101
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


class _StreamConsType(Stream):

    def __new__(cls, head, tail):
        if not isinstance(tail, LazyValue):
            raise TypeError("'tail' should be lazy value")
        obj = object.__new__(cls)
        obj._head = head
        obj._tail_lazy = tail
        return obj

    @property
    def head(self):
        return self._head

    @property
    def tail(self):
        value = self._tail_lazy.value
        if not isinstance(value, Stream):
            raise AttributeError('The tail evaluator returned invalid type')
        return value

    def __bool__(self):
        return True

    def _map_tail_lazy(self, func):
        return generic_map(func, self._tail_lazy)


Stream.empty = Stream.get_empty()

for cls in (_StreamEmptyType, _StreamConsType):
    cls.__internal_name__ = cls.__name__
    cls.__name__ = Stream.__name__
    cls.__qualname__ = Stream.__qualname__
