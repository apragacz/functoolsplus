import abc

from functoolsplus.utils.singletons import Missing


class Functor(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __map__(self, func):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Functor:
            return _check_methods(C, '__map__')
        return NotImplemented


class Monad(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __flatmap__(self, func):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Monad:
            return _check_methods(C, '__flatmap__', '__unit__')
        return NotImplemented

    @staticmethod
    @abc.abstractmethod
    def __unit__(cls, value):
        return NotImplemented


class Filterable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __filter__(self, func):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Filterable:
            return _check_methods(C, '__filter__')
        return NotImplemented


class Foldable(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __fold__(self, func, *, initial_value=Missing):
        return NotImplemented

    @classmethod
    def __subclasshook__(cls, C):
        if cls is Foldable:
            return _check_methods(C, '__fold__')
        return NotImplemented


def _check_methods(C, *methods):
    mro = C.__mro__
    for method in methods:
        for B in mro:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                break
        else:
            return NotImplemented
    return True
