from functools import partial

import pytest
from hypothesis import given
from hypothesis import strategies as st

from functoolsplus import filter, map
from functoolsplus.containers.pipes import P


def test_chain_methods_cons():
    pipe = (
        P
        .filter(lambda x: x % 2 == 1)
        .map(lambda x: x + 1)
        .sum()
        .to_type(float))
    result = pipe([1, 2, 3, 4, 5])
    assert result == 12.0
    assert isinstance(result, float)


def test_operator_cons():
    pipe = (
        P |
        partial(filter, lambda x: x % 2 == 1) |
        partial(map, lambda x: x + 1) |
        sum |
        float)
    result = pipe([1, 2, 3, 4, 5])
    assert result == 12.0
    assert isinstance(result, float)


@given(st.lists(st.integers()))
def test_concat_with_another_pipe(input_list):
    pipe1 = P | partial(map, lambda x: x + 1)
    pipe2 = P | partial(map, lambda x: x * 2)
    pipe12 = pipe1 | pipe2
    pipe21 = pipe2 | pipe1
    pipe22 = pipe2 | pipe2
    assert pipe12(input_list) == [2 * (x + 1) for x in input_list]
    assert pipe21(input_list) == [2 * x + 1 for x in input_list]
    assert pipe22(input_list) == [4 * x for x in input_list]


@given(st.text())
def test_concat_with_str(input_str):
    with pytest.raises(TypeError):
        P | input_str
