from functools import partial

from hypothesis import strategies as st

from tests.functions import always_false, always_true, identity


def build_add_function(n):
    return set_function_name(f'add_{_integer_to_id(n)}')(lambda x: x + n)


def build_mul_function(n):
    return set_function_name(f'mul_{_integer_to_id(n)}')(lambda x: x * n)


def build_mod_predicate(n):
    return set_function_name(f'mod_{_integer_to_id(n)}')(lambda x: x % n == 0)


def build_lt_predicate(n):
    return set_function_name(f'lt_{_integer_to_id(n)}')(lambda x: x < n)


def build_gt_predicate(n):
    return set_function_name(f'gt_{_integer_to_id(n)}')(lambda x: x > n)


def build_expand_function(container_cls, function_list):
    return lambda x: container_cls(f(x) for f in function_list)


@st.cacheable
@st.defines_strategy_with_reusable_values
def integer_functions():
    return (
        st.just(identity) |
        st.integers().map(build_add_function) |
        st.integers().map(build_mul_function)
    )


@st.cacheable
@st.defines_strategy_with_reusable_values
def integer_predicates():
    return (
        st.just(always_false) |
        st.just(always_true) |
        st.integers(min_value=2).map(build_mod_predicate) |
        st.integers().map(build_lt_predicate) |
        st.integers().map(build_gt_predicate)
    )


@st.defines_strategy_with_reusable_values
def integer_expand_functions(container_cls):
    return _expand_functions(integer_functions(), container_cls)


def _expand_functions(functions_strategy, container_cls):
    return (
        st.lists(functions_strategy)
        .map(partial(build_expand_function, container_cls))
    )


def set_function_name(name):

    def decorator(f):
        f.__name__ = name
        f.__qualname__ = name
        return f

    return decorator


def _integer_to_id(n):
    if n < 0:
        return f'minus_{abs(n)}'
    else:
        return f'{n}'
