from collections import OrderedDict, defaultdict, namedtuple

ImplEntry = namedtuple('ImplEntry', [
    'base_cls',
    'impl_cls',
])

_impementations_registry = defaultdict(OrderedDict)


def provide_impl_for(abc_class, base_class):

    def decorator(impl_cls):

        impl_reg = _impementations_registry[abc_class.__qualname__]
        impl_reg[base_class.__qualname__] = ImplEntry(
            base_cls=base_class,
            impl_cls=impl_cls)
        return impl_cls

    return decorator


def get_impl(abc_class, cls):
    impl_reg = _impementations_registry[abc_class.__qualname__]
    for test_cls in cls.mro():
        if test_cls.__qualname__ in impl_reg:
            return impl_reg[test_cls.__qualname__].impl_cls

    # For "virtual" base classes, which may not be in the MRO.
    for impl_entry in impl_reg.values():
        if issubclass(cls, impl_entry.base_cls):
            return impl_entry.impl_cls

    raise TypeError(
        f'No implementation of {abc_class.__name__}'
        f' for {cls.__name__} provided')
