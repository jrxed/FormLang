import pytest

from formlang20 import find_max_len_of_identical_symbols_in_reg_exp as func

def test_function():
    regexp1 = 'ab + c.aba. * .bac. + . + *'
    target1 = 'a'

    assert func(regexp1, target1) == '2'

    regexp2 = 'acb..bab.c.* .ab.ba. + . + *a.'
    target2 = 'a'

    assert func(regexp2, target2) == '2'

def test_function_inf():
    regexp1 = 'a*'
    target1 = 'a'

    assert func(regexp1, target1) == 'INF'

    regexp2 = 'ab+*'
    target2 = 'b'

    assert func(regexp2, target2) == 'INF'

    regexp2 = 'ab.b+*'
    target2 = 'b'

    assert func(regexp2, target2) == 'INF'

def test_function_error():
    regexp1 = 'aaa'
    with pytest.raises(ValueError):
        func(regexp1, 'a')

    regexp2 = '. ab'
    with pytest.raises(ValueError):
        func(regexp2, 'a')

    regexp2 = '*'
    with pytest.raises(ValueError):
        func(regexp2, 'a')
