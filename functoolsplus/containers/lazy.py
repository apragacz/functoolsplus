from functoolsplus.abc import Functor
from functoolsplus.utils.singletons import new_singleton


class UnevaluatedType(object):

    def __new__(cls):
        return new_singleton(cls)

    def __repr__(self):
        return '<unevaluated>'

    def __str__(self):
        return repr(self)


Unevaluated = UnevaluatedType()


class LazyValue(Functor):

    def __init__(self, value_evaluator=None, *, value=Unevaluated):
        if not (bool(value is not Unevaluated) ^
                bool(value_evaluator is not None)):
            raise ValueError(
                "You need to provide either value_evaluator or value"
                " exclusively")
        self._value_eval = value_evaluator
        self._value = value

    @property
    def value(self):
        if not self.is_evaluated():
            self._value = self._value_eval()
        return self._value

    @property
    def raw_value(self):
        return self._value

    def __map__(self, func):
        cls = type(self)
        return cls(lambda: func(self.value))

    def __repr__(self):
        return f'{type(self).__name__}({self._value!r})'

    def __str__(self):
        return repr(self)

    def is_evaluated(self):
        return self._value is not Unevaluated
