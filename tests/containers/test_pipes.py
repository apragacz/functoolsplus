from functools import partial

from functoolsplus import filter, map
from functoolsplus.containers.pipes import P


def test_pipe_chain_methods_cons():
    pipe = (
        P
        .filter(lambda x: x % 2 == 1)
        .map(lambda x: x + 1)
        .sum()
        .to_type(float))
    result = pipe([1, 2, 3, 4, 5])
    assert result == 12.0
    assert isinstance(result, float)


def test_pipe_operator_cons():
    pipe = (
        P |
        partial(filter, lambda x: x % 2 == 1) |
        partial(map, lambda x: x + 1) |
        sum |
        float)
    result = pipe([1, 2, 3, 4, 5])
    assert result == 12.0
    assert isinstance(result, float)
