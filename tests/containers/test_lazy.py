import pytest

from functoolsplus.containers.lazy import LazyValue, Unevaluated


def test_with_value_evaluator():
    lv = LazyValue(lambda: 42)
    assert not lv.is_evaluated()
    assert lv.raw_value is Unevaluated
    assert str(lv) == 'LazyValue(<unevaluated>)'

    value = lv.value
    assert value == 42
    assert lv.is_evaluated()
    assert lv.raw_value == value
    assert str(lv) == 'LazyValue(42)'

    assert lv.value == value
    assert lv.is_evaluated()
    assert lv.raw_value == value


def test_with_value():
    lv = LazyValue(value=42)
    assert lv.is_evaluated()
    assert lv.raw_value == 42

    value = lv.value
    assert value == 42
    assert lv.is_evaluated()
    assert lv.raw_value == value

    assert lv.value == value
    assert lv.is_evaluated()
    assert lv.raw_value == value


def test_with_value_evaluator_and_value():
    with pytest.raises(ValueError):
        LazyValue(lambda: 42, value=42)


def test_with_no_params():
    with pytest.raises(ValueError):
        LazyValue()


def test_unevaluated_str():
    assert str(Unevaluated) == '<unevaluated>'
