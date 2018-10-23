import abc
from collections.abc import Iterable
from itertools import islice

from functoolsplus.abc import Functor


class SingleLinkedStruct(Iterable, Functor):

    @classmethod
    @abc.abstractclassmethod
    def get_empty(cls):
        raise NotImplementedError()

    @classmethod
    @abc.abstractclassmethod
    def cons(cls, head, tail):
        raise NotImplementedError()

    @classmethod
    @abc.abstractclassmethod
    def cons_simple(cls, head, tail):
        raise NotImplementedError()

    @classmethod
    def from_iterable(cls, iterable):
        lst = cls.get_empty()
        for item in reversed(iterable):
            lst = cls.cons_simple(item, lst)
        return lst

    @property
    def head(self):
        raise AttributeError(
            f"type object {type(self).__name__!r} has no attribute 'head'")

    @property
    def tail(self):
        raise AttributeError(
            f"type object {type(self).__name__!r} has no attribute 'tail'")

    def __iter__(self):
        current = self
        while current:
            yield current.head
            current = current.tail

    def __repr__(self):
        items = self._get_repr_items()
        return f'{type(self).__name__}({items!r})'

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return list(islice(self, index.start, index.stop, index.step))
        if isinstance(index, int):
            elem = next(islice(self, index, index + 1))
            return elem
        raise TypeError(
            f"{type(self).__name__!r} indices must be integers or slices,"
            f" not {type(index).__name__!r}")

    @abc.abstractmethod
    def _get_repr_items(self):
        raise NotImplementedError()
