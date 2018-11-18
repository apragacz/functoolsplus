import abc
from collections.abc import Iterable, Reversible
from itertools import islice

from functoolsplus.abc import Filterable, Functor, Monad


class SingleLinkedStruct(Iterable, Filterable, Functor, Monad):

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
        if not isinstance(iterable, Reversible):
            iterable = list(iterable)
        lst = cls.get_empty()
        for item in reversed(iterable):
            lst = cls.cons_simple(item, lst)
        return lst

    @staticmethod
    def __unit__(cls, value):
        return cls.cons_simple(value, cls.get_empty())

    @property
    def head(self):
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute 'head'")

    @property
    def tail(self):
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute 'tail'")

    def __iter__(self):
        current = self
        while current:
            yield current.head
            current = current.tail

    def __repr__(self):
        items = self._get_repr_items()
        if items:
            return f'{type(self).__name__}({items!r})'
        else:
            return f'{type(self).__name__}()'

    def __str__(self):
        return repr(self)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return self.from_iterable(
                islice(self, index.start, index.stop, index.step))
        if isinstance(index, int):
            try:
                return next(islice(self, index, index + 1))
            except (StopIteration, ValueError):
                raise IndexError('list index out of range')
        raise TypeError(
            f"{type(self).__name__!r} indices must be integers or slices,"
            f" not {type(index).__name__!r}")

    @abc.abstractmethod
    def _get_repr_items(self):
        raise NotImplementedError()
