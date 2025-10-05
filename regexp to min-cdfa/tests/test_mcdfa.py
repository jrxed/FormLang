import pytest

from src.mcdfa import MCDFA


def test_manual():
    sigma = ('a', 'b')

    reg1 = 'ababaabababbabbabba'
    aut1 = MCDFA(reg1, sigma)
    assert len(aut1.states) == len(reg1) + 2

    reg2 = '(a|b)*|a'
    aut2 = MCDFA(reg2, sigma)
    assert len(aut2.states) == 1 and aut2.final == {0}

    aut2.make_complementary()
    assert not aut2.final

    reg3 = '(((ε|ε)*)+|(ε*ε+)*)*'
    aut3 = MCDFA(reg3, sigma)
    aut3.make_complementary()
    print(aut3.get_config())
    assert len(aut3.states) == 2 and aut3.final == {1}

    reg4 = 'a|v|c'
    aut4 = MCDFA(reg4, ('a', 'c', 'v'))
    assert aut4.sigma == ('a', 'c', 'v') and len(aut4.states) == 3

    reg5 = '(ab|ba)*(ε|a|ba)'
    aut5 = MCDFA(reg5, sigma)
    assert aut5.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3],
        'final': {0, 1},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 2, 'sym': 'b'},
            {'from': 1, 'to': 3, 'sym': 'a'},
            {'from': 1, 'to': 0, 'sym': 'b'},
            {'from': 2, 'to': 0, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 3, 'sym': 'a'},
            {'from': 3, 'to': 3, 'sym': 'b'},
        ]
    }

    reg6 = '(a(ab|b(ba)*a)*)*'
    aut6 = MCDFA(reg6, sigma)
    aut6.make_complementary()
    assert aut6.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3, 4, 5],
        'final': {3, 4, 5},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 5, 'sym': 'b'},
            {'from': 1, 'to': 2, 'sym': 'a'},
            {'from': 1, 'to': 3, 'sym': 'b'},
            {'from': 2, 'to': 2, 'sym': 'a'},
            {'from': 2, 'to': 1, 'sym': 'b'},
            {'from': 3, 'to': 1, 'sym': 'a'},
            {'from': 3, 'to': 4, 'sym': 'b'},
            {'from': 4, 'to': 3, 'sym': 'a'},
            {'from': 4, 'to': 5, 'sym': 'b'},
            {'from': 5, 'to': 5, 'sym': 'a'},
            {'from': 5, 'to': 5, 'sym': 'b'},
        ]
    }

    reg7 = '(ab)*a*|((a|b)(a|b))*'
    aut7 = MCDFA(reg7, sigma)
    aut7.make_complementary()
    assert aut7.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3, 4, 5],
        'final': {2},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 2, 'sym': 'b'},
            {'from': 1, 'to': 3, 'sym': 'a'},
            {'from': 1, 'to': 0, 'sym': 'b'},
            {'from': 2, 'to': 4, 'sym': 'a'},
            {'from': 2, 'to': 4, 'sym': 'b'},
            {'from': 3, 'to': 5, 'sym': 'a'},
            {'from': 3, 'to': 2, 'sym': 'b'},
            {'from': 4, 'to': 2, 'sym': 'a'},
            {'from': 4, 'to': 2, 'sym': 'b'},
            {'from': 5, 'to': 3, 'sym': 'a'},
            {'from': 5, 'to': 4, 'sym': 'b'},
        ]
    }

    reg8  = '(a|b)+bab(a|b)+'
    aut8 = MCDFA(reg8, sigma)
    aut8.make_complementary()
    assert aut8.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3, 4, 5],
        'final': {0, 1, 2, 3, 4},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 1, 'sym': 'b'},
            {'from': 1, 'to': 1, 'sym': 'a'},
            {'from': 1, 'to': 2, 'sym': 'b'},
            {'from': 2, 'to': 3, 'sym': 'a'},
            {'from': 2, 'to': 2, 'sym': 'b'},
            {'from': 3, 'to': 1, 'sym': 'a'},
            {'from': 3, 'to': 4, 'sym': 'b'},
            {'from': 4, 'to': 5, 'sym': 'a'},
            {'from': 4, 'to': 5, 'sym': 'b'},
            {'from': 5, 'to': 5, 'sym': 'a'},
            {'from': 5, 'to': 5, 'sym': 'b'},
        ]
    }

def test_internet_examples():
    # examples on https://cyberzhg.github.io/toolbox/
    sigma = ('a', 'b')

    config_aut_with_all_words = {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0],
        'final': {0},
        'delta': [
            {'from': 0, 'to': 0, 'sym': 'a'},
            {'from': 0, 'to': 0, 'sym': 'b'}
        ]
    }

    example1 = '(a|b)*'
    aut1 = MCDFA(example1, sigma)
    assert aut1.get_config() == config_aut_with_all_words

    example2 = '(a*|b*)*'
    aut2 = MCDFA(example2, sigma)
    assert aut2.get_config() == config_aut_with_all_words

    example3 = '((ε|a)b*)*'
    aut3 = MCDFA(example3, sigma)
    assert aut3.get_config() == config_aut_with_all_words

    example4 = '(a|b)*abb(a|b)*'
    aut4 = MCDFA(example4, sigma)
    assert aut4.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3],
        'final': {3},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 0, 'sym': 'b'},
            {'from': 1, 'to': 1, 'sym': 'a'},
            {'from': 1, 'to': 2, 'sym': 'b'},
            {'from': 2, 'to': 1, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 3, 'sym': 'a'},
            {'from': 3, 'to': 3, 'sym': 'b'}
        ]
    }

def test_epsilon():
    sigma = ('a', 'b')

    reg1 = '(ε|ε+ε*)|(ε|(ε|(ε)))*εεε(ε|ε)ε+'
    aut1 = MCDFA(reg1, sigma)
    assert aut1.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1],
        'final': {0},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 1, 'sym': 'b'},
            {'from': 1, 'to': 1, 'sym': 'a'},
            {'from': 1, 'to': 1, 'sym': 'b'},
        ]
    }

    aut1.make_complementary()
    assert aut1.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1],
        'final': {1},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 1, 'sym': 'b'},
            {'from': 1, 'to': 1, 'sym': 'a'},
            {'from': 1, 'to': 1, 'sym': 'b'},
        ]
    }
    
    reg2 = reg1 + 'ab' # same as ε|εab == (ε)|(ab)
    aut2 = MCDFA(reg2, sigma)
    assert aut2.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3],
        'final': {0, 2},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 3, 'sym': 'b'},
            {'from': 1, 'to': 3, 'sym': 'a'},
            {'from': 1, 'to': 2, 'sym': 'b'},
            {'from': 2, 'to': 3, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 3, 'sym': 'a'},
            {'from': 3, 'to': 3, 'sym': 'b'},
        ]
    }

    reg3 = reg2 + reg1
    aut3 = MCDFA(reg3, sigma)
    assert aut3.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3],
        'final': {0, 2},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 3, 'sym': 'b'},
            {'from': 1, 'to': 3, 'sym': 'a'},
            {'from': 1, 'to': 2, 'sym': 'b'},
            {'from': 2, 'to': 3, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 3, 'sym': 'a'},
            {'from': 3, 'to': 3, 'sym': 'b'},
        ]
    }

def test_advanced_cases():
    sigma = ('a', 'b')

    reg1 = 'ab(bb+b*(a|aaa|b)*)+b|a'
    aut1 = MCDFA(reg1, sigma)
    assert aut1.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3, 4, 5, 6],
        'final': {1, 5},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 6, 'sym': 'b'},
            {'from': 1, 'to': 6, 'sym': 'a'},
            {'from': 1, 'to': 2, 'sym': 'b'},
            {'from': 2, 'to': 6, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 6, 'sym': 'a'},
            {'from': 3, 'to': 4, 'sym': 'b'},
            {'from': 4, 'to': 4, 'sym': 'a'},
            {'from': 4, 'to': 5, 'sym': 'b'},
            {'from': 5, 'to': 4, 'sym': 'a'},
            {'from': 5, 'to': 5, 'sym': 'b'},
            {'from': 6, 'to': 6, 'sym': 'a'},
            {'from': 6, 'to': 6, 'sym': 'b'}
        ]
    }

    reg2 = '((ba|ab*)+|(baa*)|(aab+a+b)*)|(ε*(a|(b(aa+ε)b)+))'
    aut2 = MCDFA(reg2, sigma)
    assert aut2.get_config() == {
        'sigma': ('a', 'b'),
        'start': 0,
        'states': [0, 1, 2, 3],
        'final': {0, 1},
        'delta': [
            {'from': 0, 'to': 1, 'sym': 'a'},
            {'from': 0, 'to': 2, 'sym': 'b'},
            {'from': 1, 'to': 1, 'sym': 'a'},
            {'from': 1, 'to': 1, 'sym': 'b'},
            {'from': 2, 'to': 0, 'sym': 'a'},
            {'from': 2, 'to': 3, 'sym': 'b'},
            {'from': 3, 'to': 3, 'sym': 'a'},
            {'from': 3, 'to': 3, 'sym': 'b'}
        ]
    }
