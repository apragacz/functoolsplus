from collections.abc import Iterable

from functoolsplus.abc import Filterable, Foldable, Functor, Monad
from functoolsplus.utils.implementations import get_impl, provide_impl_for
from functoolsplus.utils.singletons import Missing


def map(func, obj):
    return _generic_higher_order_func(Functor, 'map', '__map__', func, obj)


def filter(func, obj):
    return _generic_higher_order_func(
        Filterable, 'filter', '__filter__', func, obj)


def fold(func, obj, *, initial_value=Missing):
    return _generic_higher_order_func(
        Foldable, 'fold', '__fold__', func, obj, initial_value=initial_value)


def flatmap(func, obj):
    return _generic_higher_order_func(
        Monad, 'flatmap', '__flatmap__', func, obj)


def _generic_higher_order_func(
        abc_cls, name, method_name, func, obj, **kwargs):

    if isinstance(obj, abc_cls):
        obj_handler = getattr(obj, method_name)
        result = obj_handler(func, **kwargs)
        if result is not NotImplemented:
            return result

    obj_type = type(obj)
    try:
        impl_cls = get_impl(abc_cls, obj_type)
    except TypeError:
        pass
    else:
        cls_handler = getattr(impl_cls, method_name)
        result = cls_handler(obj, func, **kwargs)
        if result is not NotImplemented:
            return result

    raise TypeError(f'{obj_type.__name__!r} does not support {name} interface')


def unit(cls, value):
    if issubclass(cls, Monad):
        result = cls.__unit__(cls, value)
        if result is not NotImplemented:
            return result

    try:
        impl_cls = get_impl(Monad, cls)
    except TypeError:
        pass
    else:
        result = impl_cls.__unit__(cls, value)
        if result is not NotImplemented:
            return result

    raise TypeError(f'{cls.__name__!r} does not support unit interface')


@provide_impl_for(Functor, Iterable)
@provide_impl_for(Filterable, Iterable)
@provide_impl_for(Foldable, Iterable)
@provide_impl_for(Monad, Iterable)
class _IterableImpl(
        Functor,
        Filterable,
        Foldable,
        Monad,
        Iterable):

    def __map__(self, func):
        cls = type(self)
        return cls(func(item) for item in self)

    def __filter__(self, func):
        cls = type(self)
        return cls(item for item in self if func(item))

    def __fold__(self, func, initial_value=Missing):
        obj_iter = iter(self)
        value = initial_value
        if value is Missing:
            try:
                value = next(obj_iter)
            except StopIteration:
                raise ValueError(
                    f'Empty {type(self).__name__!r} object'
                    f' but no initial value provided')

        for item in obj_iter:
            value = func(value, item)

        return value

    def __flatmap__(self, func):
        cls = type(self)
        return cls(_flatmap_iter(self, func))

    @staticmethod
    def __unit__(cls, value):
        return cls([value])


def _flatmap_iter(obj, func):
    for item in obj:
        for result_item in func(item):
            yield result_item
