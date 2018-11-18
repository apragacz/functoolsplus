from collections.abc import Callable, Mapping
from functools import partial

from functoolsplus.hof import filter as generic_filter
from functoolsplus.hof import flatmap, fold
from functoolsplus.hof import map as generic_map
from functoolsplus.utils.singletons import Missing


class PipeRegistry(Mapping):

    def __init__(self):
        self._registry = {}

    def __getitem__(self, key):
        return self._registry[key]

    def __iter__(self):
        return iter(self._registry)

    def __len__(self):
        return len(self._registry)

    def register(self, name, func):
        obj = self._clone()
        obj._registry[name] = func
        return obj

    def _clone(self):
        cls = type(self)
        obj = cls()
        obj._registry = self._registry.copy()
        return obj


default_registry = (
    PipeRegistry()
    .register('map', generic_map)
    .register('filter', generic_filter)
    .register('flatmap', flatmap)
    .register('fold', fold)
    .register('len', len)
    .register('sum', sum)
    .register('min', min)
    .register('max', max)
    .register('imap', map)
    .register('ifilter', filter)
)


class Pipe(Callable):

    def __init__(self, input_value=Missing, registry=default_registry):
        self._steps = []
        self._registry = registry
        self._input_value = input_value

    def __or__(self, other):
        if isinstance(other, Pipe):
            obj = self._clone()
            obj._steps.extend(other._steps)
            assert other._input_value is Missing
            return obj
        elif callable(other):
            return self.step(other)
        return NotImplemented

    def __getattr__(self, name):

        def func(*args, **kwargs):
            obj = args[-1]
            if not hasattr(obj, name) and name in self._registry:
                f = self._registry[name]
            else:
                f = getattr(obj, name)
            return f(*args, **kwargs)

        return PipeCall(self, func)

    def step(self, func):
        obj = self._clone()
        obj._steps.append(func)
        return obj

    def to_type(self, type_):
        return self.step(type_)

    def _clone(self):
        cls = type(self)
        obj = cls()
        obj._steps = self._steps[:]
        obj._registry = self._registry
        obj._input_value = self._input_value
        return obj

    def __call__(self, input_value):
        value = input_value
        for f in self._steps:
            value = f(value)
        return value


class PipeCall(Callable):

    def __init__(self, pipe, func):
        self._pipe = pipe
        self._func = func

    def __call__(self, *args, **kwargs):
        step_func = partial(self._func, *args, **kwargs)
        return self._pipe.step(step_func)


P = Pipe()
