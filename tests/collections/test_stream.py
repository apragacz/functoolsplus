from hypothesis import given
from hypothesis import strategies as st

from functoolsplus.collections import Stream


def test_empty_stream_is_a_singleton():
    assert Stream() is Stream.empty
    assert Stream([]) is Stream.empty


@given(st.lists(st.integers()))
def test_isinstance(input_list):
    lst = Stream(input_list)
    assert isinstance(lst, Stream)
