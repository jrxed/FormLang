import pytest

from formlang20 import *


def test_int_init():
    a = IntWithInf()

    with pytest.raises(TypeError):
        b = IntWithInf('hello')
    with pytest.raises(TypeError):
        c = IntWithInf(3.14)

    d = IntWithInf(a)

def test_int_sum():
    a = IntWithInf(120)
    b = IntWithInf(47)

    c = a + b
    assert not c.is_infinite() and c.int() == a.int() + b.int() and c.int() == 167

def test_int_inf():
    inf = IntWithInf('INF')
    with pytest.raises(ValueError):
        num = inf.int()

    a = IntWithInf(120)

    inf_sum = inf + a
    assert inf_sum.is_infinite()

    inf_sum = inf_sum + inf_sum
    assert inf_sum.is_infinite()

def test_int_bool():
    zero = IntWithInf()
    assert not zero

    one = IntWithInf(1)
    assert one

def test_int_eq():
    a = IntWithInf(120)
    b = IntWithInf(47)
    c = a + b

    copy = IntWithInf(c)

    expected = IntWithInf(167)

    inf = IntWithInf('INF')

    zero = IntWithInf()

    assert a == a
    assert c == c
    assert c == expected
    assert c == copy
    assert inf == inf
    assert not a == inf

    assert a == 120
    assert b == 47
    assert not a == 47
    assert c == 167
    assert not inf == 0
    assert zero == 0

def test_int_max():
    a = IntWithInf(120)
    b = IntWithInf(47)
    c = a + b

    inf = IntWithInf('INF')

    assert IntWithInf.max(a) == a
    assert IntWithInf.max(a, b) == a
    assert IntWithInf.max(a, b, c, inf) == inf
    assert IntWithInf.max(a, b, c) == c

    with pytest.raises(TypeError):
        IntWithInf.max()

def test_int_repr():
    a = IntWithInf(120)
    b = IntWithInf(47)

    inf = IntWithInf('INF')

    assert str(a) == '120'
    assert str(b) == '47'
    assert str(inf) == 'INF'
