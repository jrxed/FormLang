import pytest

from formlang20 import *


def test_counter_init():
    counter_a_cls = CounterFactory.get_counter('a')
    counter_b_cls = CounterFactory.get_counter('b')

    assert counter_a_cls != counter_b_cls

    counter_a1 = counter_a_cls('a')
    counter_b1 = counter_b_cls('b')
    assert counter_a1.get_count() == [0, 0, 0, 1]
    assert counter_b1.get_count() == [0, 0, 0, 1]

    counter_a2 = counter_a_cls('b')
    counter_a3 = counter_a_cls('c')
    counter_a4 = counter_a_cls()
    assert counter_a2.get_count() == [0, 0, 0, 0]
    assert counter_a3.get_count() == [0, 0, 0, 0]
    assert counter_a4.get_count() == [0, 0, 0, 0]

def test_counter_star():
    counter_a_cls = CounterFactory.get_counter('a')

    counter1 = counter_a_cls()
    counter1.set_count((1, 3, 8, 0))
    counter1.star()
    assert counter1.get_count() == [11, 3, 8, 0]

    counter2 = counter_a_cls()
    counter2.set_count((1, 3, 0, 0))
    counter2.star()
    assert counter2.get_count() == [1, 3, 0, 0]

    counter3 = counter_a_cls()
    counter3.set_count((1, 0, 8, 0))
    counter3.star()
    assert counter3.get_count() == [1, 0, 8, 0]

    counter1 = counter_a_cls()
    counter1.star()
    assert counter1.get_count() == [0, 0, 0, 0]

def test_counter_star_inf():
    counter_a_cls = CounterFactory.get_counter('a')

    inf = IntWithInf('INF')

    counter1 = counter_a_cls()
    counter1.set_count((1, 0, 0, 1))
    counter1.star()
    assert counter1.get_count() == [1, 0, 0, inf]

    counter2 = counter_a_cls()
    counter2.set_count((1, 3, 8, 1))
    counter2.star()
    assert counter2.get_count() == [inf, inf, inf, inf]

    counter3 = counter_a_cls()
    counter3.set_count((0, 0, 0, 1))
    counter3.star()
    assert counter3.get_count() == [0, 0, 0, inf]

    counter4 = counter_a_cls()
    counter4.set_count((0, 1, 0, 1))
    counter4.star()
    assert counter4.get_count() == [0, inf, 0, inf]

    counter5 = counter_a_cls()
    counter5.set_count((0, 0, 1, 1))
    counter5.star()
    assert counter5.get_count() == [0, 0, inf, inf]

def test_set_get_count_clear():
    counter_a_cls = CounterFactory.get_counter('a')

    counter = counter_a_cls()
    assert counter.get_count() == [0, 0, 0, 0]

    counter.set_count((1, 3, 8, 0))
    assert counter.get_count() == [1, 3, 8, 0]

    counter.clear()
    assert counter.get_count() == [0, 0, 0, 0]

    with pytest.raises(ValueError):
        counter.set_count((1, 0, 8, 0, 2))
    with pytest.raises(ValueError):
        counter.set_count((1, 0, 8))
    with pytest.raises(ValueError):
        counter.set_count('hello')
    with pytest.raises(TypeError):
        counter.set_count(5)
    with pytest.raises(TypeError):
        counter.set_count()

def test_add():
    counter_a_cls = CounterFactory.get_counter('a')
    inf = IntWithInf('INF')

    counter1 = counter_a_cls()
    counter1.set_count((1, 3, 8, 7))

    counter2 = counter_a_cls()
    counter2.set_count((5, 6, 100, 9))
    assert (counter1 + counter2).get_count() == [5, 6, 100, 9]
    assert (counter2 + counter1).get_count() == [5, 6, 100, 9]

    counter3 = counter_a_cls()
    counter3.set_count((inf, inf, inf, inf))
    assert (counter2 + counter3).get_count() == [inf, inf, inf, inf]

    counter4 = counter_a_cls()
    counter4.set_count((6, 2, 50, 50))
    assert (counter2 + counter4).get_count() == [6, 6, 100, 50]

    with pytest.raises(TypeError):
        counter4 += 2

def test_mul():
    counter_a_cls = CounterFactory.get_counter('a')

    counter1 = counter_a_cls()
    counter1.set_count((1, 3, 8, 7))

    counter2 = counter_a_cls()
    counter2.set_count((5, 6, 100, 9))

    counter3 = counter_a_cls()
    counter3.set_count((17, 4, 40, 0))

    assert (counter1 * counter2).get_count() == [14, 13, 100, 16]
    assert (counter2 * counter1).get_count() == [103, 12, 107, 16]

    assert (counter1 * counter3).get_count() == [17, 11, 40, 0]
    assert (counter3 * counter1).get_count() == [43, 4, 47, 0]

    assert (counter3 * counter2).get_count() == [46, 4, 100, 0]
    assert (counter2 * counter3).get_count() == [104, 13, 40, 0]

    counter4 = counter_a_cls('1')
    counter4.set_count((6, 2, 0, 0))

    assert (counter2 * counter4).get_count() == [102, 11, 100, 9]
    assert (counter4 * counter2).get_count() == [6, 9, 100, 9]

    with pytest.raises(TypeError):
        counter1 *= 2

def test_repr():
    counter_a_cls = CounterFactory.get_counter('a')

    counter = counter_a_cls()
    assert str(counter) == str([0, 0, 0, 0])

    counter.set_count((1, 3, 8, 7))
    assert str(counter) == str([1, 3, 8, 7])

    counter.star()
    assert str(counter) == '[' + ', '.join(('INF',) * 4) + ']'

def test_empty():
    counter_a_cls = CounterFactory.get_counter('a')

    counter1 = counter_a_cls()
    counter1.set_contains_empty(True)

    counter2 = counter_a_cls()

    assert (counter1 + counter2).contains_empty()
    assert (counter1 + counter1).contains_empty()
    assert not (counter2 + counter2).contains_empty()

    assert not (counter1 * counter2).contains_empty()
    assert not (counter2 * counter1).contains_empty()
    assert (counter1 * counter1).contains_empty()
    assert not (counter2 + counter2).contains_empty()

    counter3 = counter_a_cls('1')
    assert counter1.contains_empty() == counter3.contains_empty()
