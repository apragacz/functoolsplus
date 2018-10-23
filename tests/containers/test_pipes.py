from functools import partial

from functoolsplus.containers.pipes import Pipe, P
from functoolsplus import filter, map


def test_pipe_chain_methods_cons():
    p = Pipe().map(lambda x: x + 1).sum().to_type(float)
    result = p([1, 2, 3, 4, 5])
    assert result == 20.0
    assert isinstance(result, float)


def test_pipe_operator_cons():
    p = P | partial(map, lambda x: x + 1) | sum | float
    result = p([1, 2, 3, 4, 5])
    assert result == 20.0
    assert isinstance(result, float)
