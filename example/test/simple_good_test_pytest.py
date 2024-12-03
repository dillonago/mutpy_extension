import pytest
from example.simple import Simple


@pytest.fixture
def simple():
    return Simple(1337)


def test_add(simple):
    assert simple.add(2, 2) == 4


def test_add_two(simple):
    assert simple.add_two(2) == 4


def test_add_etc(simple):
    assert simple.add_etc("ala, kot, pies") == "ala, kot, pies etc."


def test_add_str(simple):
    assert simple.add("ala", "kota") == "alakota"


def test_loop(simple):
    assert simple.loop() == 100


def test_last_two(simple):
    assert simple.last_two([1, 2, 3, 4]) == [3, 4]


def test_empty_string(simple):
    assert simple.empty_string() == ""


def test_get_const(simple):
    assert simple.get_const() == 1337


def test_get_inc_const(simple):
    assert simple.get_inc_const() == 1338
    assert Simple.get_inc_const() == 1338


def test_get_magic(simple):
    assert simple.get_magic() == 1337


def test_is_odd(simple):
    assert simple.is_odd(1) is True


def test_is_not_odd(simple):
    assert simple.is_odd(2) is False


def test_negate_number(simple):
    assert simple.negate_number(10) == -10


def test_negate_bool(simple):
    assert simple.negate_bool(True) is False


def test_negate_bitwise(simple):
    assert simple.negate_bitwise(1) == -2


def test_bool_conjunction(simple):
    assert simple.bool_conjunction(True, False) is True


def test_bitwise_conjunction(simple):
    assert simple.bitwise_conjunction(1, 0) == 1


def test_override(simple):
    assert simple.foo() == 2


def test_overridden_call(simple):
    simple.bar()
    assert simple.x == 2


def test_handle_exception(simple):
    assert simple.handle_exception() == 1


def test_class_variable(simple):
    assert simple.X == 2
