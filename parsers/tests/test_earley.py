import copy

import pytest

from earley import Earley


def test_state():
    head = 'S'
    body = 'aSbS'
    i = 0
    j = 0
    dot_index = 0
    state = Earley.State(head, body, i, j, dot_index)

    state_copy_completed = copy.deepcopy(state)
    state_copy_completed.is_completed = True

    state_copy_predicted = copy.deepcopy(state)
    state_copy_predicted.is_predicted = True

    state_copy_completed_predicted = copy.deepcopy(state)
    state_copy_completed_predicted.is_completed = True
    state_copy_completed_predicted.is_predicted = True

    s = set()
    s.add(state)
    s.add(state_copy_completed)
    s.add(state_copy_predicted)
    s.add(state_copy_completed_predicted)

    assert len(s) == 1

def test_basic():
    parser = Earley()
    parser.fit(
        'S',
        'ab',
        (
            ('S', 'aSbS'),
            ('S', '')
        ),
        'S'
    )

    words = (
        'aababb',
        'aabbba'
    )
    expected = [True, False]
    actual = map(parser.predict, words)
    assert parser.predict(words[0]) == expected[0]
    assert parser.predict(words[1]) == expected[1]
    assert all((x == y for x, y in zip(expected, actual)))

def test_a_eq_2b():
    parser = Earley()
    parser.fit(
        'S',
        'ab',
        (
            ('S', 'bSaSaS'),
            ('S', 'aSbSaS'),
            ('S', 'aSaSbS'),
            ('S', '')
        ),
        'S'
    )

    words_positive = map(str.strip, ('''
        aba
        baa
        aabaaaaabaabbab
        baaabbaaa
        
        abaabaaba
        aabaaabab
        aab
        baaaababbaabaaa
        abaaba
    ''').strip().split('\n'))

    words_negative = map(str.strip, ('''
        bbbbbbbbb
        bbba
        bbabababbaaaba
        bbababbabaaba
        bbaababbaba
        bbabaaaababbabb
        abababaabbbba
        baaabaab
        bbababaab
        ababbba
    ''').strip().split('\n'))

    assert all(map(parser.predict, words_positive))
    assert not any(map(parser.predict, words_negative))

def test_a_eq_b_plus_1():
    parser = Earley()
    parser.fit(
        'S',
        'ab',
        (
            ('S', 'bSS'),
            ('S', 'SbS'),
            ('S', 'SSb'),
            ('S', 'a')
        ),
        'S'
    )

    words_positive = map(str.strip, ('''
        a
        abaababbaba
        abaabba
        bbaaa
        bbaaabaabab
        baa
        abaaabb
        abbabaabababaab
        bbaababaa
        bababaaba
    ''').strip().split('\n'))

    words_negative = map(str.strip, ('''
        aabbaabbabaaba
        ababbbba
        baabbabbba
        aabbbb
        aaabbababbbbba
        aaababbb
        babbbbbabbbba
        abaabaaba
        babaab
        aaabbbaabb
    ''').strip().split('\n'))

    assert all(map(parser.predict, words_positive))
    assert not any(map(parser.predict, words_negative))

def test_palindrome():
    parser = Earley()
    parser.fit(
        'S',
        'abc',
        (
            ('S', 'aSa'),
            ('S', 'bSb'),
            ('S', 'cSc'),
            ('S', 'a'),
            ('S', 'b'),
            ('S', 'c'),
            ('S', '')
        ),
        'S'
    )

    words_positive = map(str.strip, ('''
        bcacb
        bcabccacaccbacb
        acbaccabaccabca
        ccbccbcc
        bacccacccab
        abbbccaccbbba
        bcababacb
        acabcacbaca
        aaacaacaaa
        bcaaaabbaaaacb
    ''').strip().split('\n'))

    words_negative = map(str.strip, ('''
        acacba
        abbcabbbcba
        bbcaacaca
        bababbcccaabcba
        cbcca
        bbac
        baccaba
        abac
        babaccbcabbc
        cbccbaccc
    ''').strip().split('\n'))

    assert all(map(parser.predict, words_positive))
    assert not any(map(parser.predict, words_negative))

def test_balanced_bracket_sequence():
    parser = Earley()
    parser.fit(
        'S',
        'ab',
        (
            ('S', 'aSbS'),
            ('S', '')
        ),
        'S'
    )

    words_positive = map(str.strip, ('''
        aaaaababbbbaababaabababbbabaabaaaaaabbbbabaaabbaabaabbbaabaabbbaababaabbbbbbabbaababbaabbabbabaabbab
        aabaaaabbbabaababaabbaaababababbaabbababbaababbbabbabaabaaaaababaabbbabaabbbabbbbaaaabbbabbbaabababb
        aaaabbaaaaaababaabaabbbbbababbbaaaaaaabaabbabbbbbbbabbaaababaaaaabaabbababbabbaababbabbababbbbbbabab
        abababaaaabaababbaababbbabaabbabaaaabbababbaabaabbabaababababbababaabababbaabaabaaabbabbbbabbbbababb
        aaabababbaaaabaaaabbabbababbabaabaabaaabaababaabbbbaabaabaabbbbbbabbabababaaabaaabbbabbbbbbaabbbaabb
        ababaababaaaabaabbbababaabbbabaaabaaababaabaabbabbababbabbaabaabbaabbabbababbababbabbabaabbaabbbaabb
        abaababbabaaabaaaaababbbaabababaaabbaabbbbaaaabbaaaabbabbaaabbabaabaabaabbabaabaabbabbbabbbbbbbbabbb
        abaabaabbabaabaabaaabbaaaaababbbbabbaaabbaabbaaaabbaabbabababaaabbbbbbabaaaaaaababaabbbbbbbbbbbaabbb
        aaaabbbaaaabbbaaababaababaabbabbaaaaaaaaababaaabbbbbbbbbaabaababbaaaaabbaababbbbbbbbbababbaababbbabb
        aababaaababaababaaaabbbaabababbabaabbaabbbbbbbaaaabbaaaabaaabbabbaabbbbababaabaabbbbbabaaaabbbaabbbb
        aaaabbaaaaababbbbabbbbababaabaaabbabbaaabaaabbbaaaabaaaabababaaaabbbbbbabababbbabbaabababbabbaabbbbb
        aabaaabaaaabbbaaababbbbaabaabaaaababaaabababbabaaabaababbabbababbbabbbbbaabaabbbaabababbabbbabababbb
        aabbaaaaaabababaaaaabbbaabbbaaabbbaaaaaaabbabbaaabbbbbbabbaaabbaabababbbabababbaaabbaabbbbbbaababbbb
        aabaabbbaaaabaaabbabbbbbaaabaaaaaabaaabbbbaabaaabbaabbaaabbbbbbabbaabababaababbaababbabbaababbbbabbb
        ababaaabbabbabaaaaabaabbbaaaabbbaabbaaabbabaabbaaaabbaababaabbbaabbaabbbabbaabaabbaaabbbbbbbabababbb
        aababaababaabbaaabaabbaabababbbaaaabaaabbaabbaabbabbaababbbbbaabbbbaababbaabababbaaababbbbaaaabbbabb
        aaabaabaabbbbabaaabbaaabaabbbababaaababaaabababbaabaabaabbbbaaabbbbaabbbbabbabbabababbaaaabaabbbabbb
        aabaabaaaabbbbaaaaaabbbaabaabbbbabbabaabaabbaabaabbabbbbaaaaaabbaabbababbbabaaabbaabbbabaabbbabbbbab
        abaabbaaabbabaaaabbbbbaaaaabaabbababbabbababaababbbaaabaaaabaabaabbbaabbbabbaaababbabaaabbabbbabbbbb
        aaabababaaabaabaaabaabbbabbaabbabbbbaaaaaaaaababababbbaabababababaaaaabababbbbbbbbabbbbabbaabbababbb
        aaaaaaabaaababbabbbabaabbabaabbaabaabbbaaabbaaaaabaababaabbbabbabbababaababababbbbabababbbbbabbababb
        aaabbaaaaababaabbaabaabbbaaababbaaaaabbabaaaaaabbababbbbbbaabaababbaabbabbbbbabaabbabbababbbbbababab
        aabaaababbbaabbaaaabbaaabbaabababbabbabaaababbbbbaaaaabbbaabbbaaabaabbbabbaabababbaaaaabbbabbbaabbbb
        aabaabbaabaabbaaabababbaaabbababaabbabbaababaaabbabbaaabbaaaababaabbbaababbbbabbbbbaabaaaabbabbbbabb
        aabaaabababaabbaabaaababaabaaaaaabbbbaabbbabbaabbbabaaaaabbbbabbbbabbaaabbabbaabababababbababbbababb
        aabaaaaabaaabbabbbbabbbaaaaaaabbbaaaaabbababaaaabaaaaabbbabbbababaabbbbabbabbbabbabbbaabbababbbaabbb
        abaababaaaabbabaabaaabbbbaababaababaabbaabbabbbbbaaaabababaaababbabbaabaaabaababbabbbbabbaabbabbbbab
        aaabbbaabaabaaaabbaaaaaabbbaaaaaababbabaabbaabbaaaabbbbbaabbabbbbbbabaabbbababaaabbbbbaabbabbaabbabb
        aaaaaaaabbaaababaaabaabaaabababbababbbaabbbaaabbbbbaaabbbabababababbbabbabababbabaabbbaaabbbbabbabab
        abaaababaababaaaabaabaaaabaaababbbabababbaabbaaaabaababbbabbabbabbbaabbbaaababbbabababaabbabbbbbbbab
        aaaaaaabaabaabbabbbbbbaaaababababaabbababbaaabaaabbbabbbaabaababbbaaabbabbaaabbababbbabbbababababbab
        aaababaabbaababaabaaabbabaabbbaaabbaabaabababaabababbabbabbbbabbaabbabbabaaaabbbababaabbbaababbbabab
        aaabbaabbaabababaabababbaababababaabaabaabbbaaabaaabaababbabbbbbbbaaabbabaaabbabaababbbaabaabbbabbbb
        aaabaaaabbaaaaababaaabaababbbabbbbababaabbababbaababbababaaababaaabbbbaabababbabaaabbbbbabbbabbaabbb
        aaabaabbababaaaaabbbbaaabaabbbbbabbaababaababaaababbaaabbbbbaabaababbaababbabbbabbabaabaabaabbaabbbb
        abaabaababaaabbaabbbababaaaaabbbabbaaababbabbaaaabbabaabaaabbbbaaababaabbbbbbaabababbaabaabbbababbbb
        aabaaaabbaaaabbabaababbabaaabbaaabaaababaaaaabaaabbbbabbaaaabbaaaabbababbabbbbaaabbbbbbbabbbbabbbbbb
        aababbabababaaaaabbaaaabbabbabaabaabbabbabaaaaaaabbababbbabaababaabbabbbbbbaaabbbabababababaaabbbbbb
        aabaaabbababbabaabaababbabaababaabababbbaaaaababbbbbaaaaaaaaaabbabbabbbaabbabbaabbbaabababaabbbbbbbb
        aabaaabbaaabbbabaaaabbaaabbbbbabaabbabaaaabbababababaaabaabababbbbaaaababaabbbabbaabbabaababbbbbbbab
        aaabaabaababbaaaabbbaabaabbaaababbbaaababababbbaababbaaaabbbaaabbbabaabbbaabbbababbabbbaaabaabbabbbb
        aaaaaabbbabaabaaaaaaabababbabbaaabbaaaaabaabbbbbaabaabbaaabbbbbaababbbbbababbabbabbabbabbaabbbaaabbb
        aabaaaaababbbbababaaaabbbbababbabababbaaabaaabbbabbaaaabbaababaaaabbbaabababbaaabaabbbabbabbbbbbabab
        aaaabaaabbabaabbbaabaabbabaaaabbbbbaaabbbaaabbabbbabaaabbabaaaaabaabaabbbabbabbababbabbbabbaabbaabbb
        abaaaaaaaaaaaaaaabbbbababababbabbbbaaaaabbbbabaaaabbbbbabbbaaaababbababbaababbbabbabbabbbababaaabbbb
        aabaaabbbaababbabaaabbaabaaaabbabbbabbaababaabaababaaabaabaabbaabbabaabababbbbbaabbbbbaabaabbbaabbbb
        aaaaaaababbbaaabaabbbabaabaabbbbabbbabaabbbabaabaabaabbaaababbaabaabaabbababaabbbbbbabaabbbaaababbbb
        aabaabbabbaaaabaaaabbabbbabaaabaaaaaabababbabaaaabaabbbbbababbabbabbbbbbbaababbaaaabababbaabbababbbb
        aaabaabaabbaababaababababababaabbbbaaabbbbaabbbabaaabbaaabbaaaabababbabbabbababaabbbbbabaababaaabbbb
        aababaabbaabbababaaabbababaabaaabaababaababbbbaaabaaaaaabbaaaaabbbbbbabaababbbbbbbbaababbabbabbabbab
        abaaaaaaabbaabbabbabaabaaababaabbbbbaaaabbbbbaaababbabbaabaaabbababbababbaabbbabbaaaabbaaabbbabbbbab
        aababaaaabababbababbbbaabbaaaaaaaaaabbbaabaabbbbababbbabbaaababbaabbaabbaabbbbbababaaaaababbababbbbb
        aabaaaabaaaaaabaabaaaabbabababbbbbabbababbabbaabaaabbbbabbbababbaaaaaababaabbbabbbbbbabaabbaaabbbbab
        aabaaaaabbbabaaaaaababaabbbbbbbbbaaaaaaaaaabbbbaaaaaabbaaaaabbaabbbbbababbbbbabbbbbabbbababaabbbaabb
        aaabaabaabababababaabbbaabababbabbaaaababaaaaaabaaabbabbbaabbbbaaabbbbabbbbbbbaababaabaaabbbaabbbbab
        aabaaabbaabaaabbabbbaaaaaaababaabaaababbabbabbbaaabbabbababbbbbbaaaaabbbabbaabaaabababbabbbbabaabbbb
        aababababaaaaababbaabaabababaabaabaaaabbabbbbabaaabbbaabbbabaaabbbbbababbaaabbbaabbababababababbbbab
        aaaaabababbababbbbabaabaaaaaaaabbbaabababbbbbbaaabbbaabbaababbbaabbbaabbabaaabbbaaabbbaabababbabaabb
        aaabbabbaaabbaabbaaaabaaabbabbbbababaabaabbaaaababaaabbabababaabaaabababbababbabbbabbaabbbababbabbbb
        abaabbaaabaaababaaabbababbbabaababaaabbbaabbbabaabbbaaabbaaabbbaaaabaaaababbabaabbbbbabbbbabbbaabbab
        aaaaaabbaabbabaabbabababaababaaaababaaabaaabbabaaabbaaabbbbabbbabbbbababbbbabbbaabbbaaabbabbaabaabbb
        aabaaababbaaaaabbbaabbaabababbbababaaabaabbaaaabbaaabbabbaabaaaabbabbaabbabbbbaaabaabbbbbaababbbbbbb
        aaabbabaabababaabaaaababbabaabaaaaaabbbabbbaaabbaaabbaabbabaabbbbabaaabbbbbbbaabbbaababbbaababbbaabb
        aaabaaaabaaabaaaaabbbbbbaababbaaabbbabbbabaabbbabaabbaaaabbabbbbabbaabbabaabbbaaabbaaaababbabbaabbbb
        abaaaaabbbaababbaabbaaabbaaabbabbbaabbaabbaababbaaabbabbabbabaabbbaababaaabaaabbabbbbaabbbaaaabbbabb
        abaabaaaaaababbbaaaababbabbaaabbabbbbaaabbaaaaaabaaabaabbabbbbbaabbabbbbbbbbaaabaaaabbaabbbbaaabbbbb
        aaaabbaaaabbbaabbabaabbaaaabaaabbabbabaabbbbbaaabbabaaaaabaaaababbbbbbbbaababbabaabaabbbaabababbbbbb
        aabaaaabaaababbaaaababbaaabbbaaabaababbaabbababbaabbbbbabaabbabaaabababbbabaababaabbbbbbbaabababbabb
        aaaabaababbbaababbbabbaaabaaabbaaaaaabbababbaabbaabbaabababbbbbaaabababbaaaabbabbbaaabbabbabbbaabbbb
        aaaababaaaaaabaaabaaabaaaaabaaaabbbabababaaabbaaabbaabbbbbbabbbbaabbabbbbaabbbabbabaababbbbabbabbbbb
        aaaabaababaaaaaabbababababbbbbabbbabaaababaaaaaabaaabbabbabbabaaaababbbaabbbbbabbbbabbbaabbabaabbbab
        aabbaaabaaabababbbaaabbbaaaabbaaaaaaabbabbbabbaaabbbbbaabaaabbbabaaaaaababbabbabaababbbabbbbbababbbb
        aaaaababbaabaabaaabaaabbbbabbaaabbaababbabaabaabbbbbababbaabbbabbbaaabababaaaababbbaaaaabbbbbbbaabbb
        aabaaabaaaaaabbabaabaaaaababbbaabaabbbbbaabababbababaabbaabbbabbbabbbaabaabbabbabbbababaaaaabbbbabbb
        aaaaabaaaaababbababaaabbabbababbabbbaabbbbabababaabaababbaabbababbabaabbbbaaaabaaababababbaabbabbbbb
        aabaaaababaabbbaaabbbbaaaabbabaaaaaaabbbababbbababbbbbabaaabaaabaaababbabbbaaaaabbbabbbbaabaabbbbbbb
        aaaaaababbaababaaaabbababbabbbaabbbababbbbaaabababaabaaaaababbbababbabaaabbababaabbbabbbabbaabaabbbb
        aaaaabaabaaaabbabbabaaabbbbaaaabbbbbbaaaaabaabbaaaaabbababbbbbbabaababbbbaabbbababbabbaababbaabbaabb
        abaabbaababbabaaaaaaabaaaabbbaaaabaaaabbbbbabababbbbbababaaaababaaabbbabaaaababbbbbbbaaaaabbbbbbbbbb
        aaaaaaaababaaabbabababbbabbbaabbabbbabaabaabaabbbaaabbaababababaabaaaababbaaaaabaabbabbbbabbbbbbbbbb
        aaaababbabbbabaababaaaaababbaabbaaaaababbaaabbabaababbbabbaaabaabbbbbabbbabaaabbbababaabaaabbabbbbbb
        aaaabbababaaaabaaabbbbbaaaaaaaaaabbbababbaabaabbbabaababbbbbaaabaaabbabababaabbbbbbaabababbbbababbbb
        aabaabababbbabaaaabbaaaaaaabbaaaababbabaabbabbaabbbaaaaabaabbbaabbbbaabbaababbbabaababbabbabbbbabbbb
        abababaaaaaaaabaabbaababbabbaaabbabaabababaaabaabbaaabaaabbaabbaabbaabbbabaaabbbbbbbbbbbbbbaabababbb
        aabaabaaaaaabaaaaaaabbbaaababbbbbaabababaaaababbaababaabaabbbabbababbbabbabbabbbbabbbabaabababbbbabb
        aaabaababaaabbbabbbabaabbbaaaabaabaabbabaabaaabaaaababababaabababaabbbbabbbaababbbbbaaabbbbabababbbb
        aaaaaabaaaabbaabbbababbaabbabaaaabaababbbbbbbabaabbbaabbaabbbababaaaaabbabbabbaababbabbaaabaabbbbabb
        abaaaaaabbbababaaaaaabbbabaababababbbbbbababaaaabbabbbaaabbaaabbbbabaababbbaabaaabababbbaaabbaabbbbb
        aaababbaaaabbbaaabbabbabaabbbaaabbabbaaabbaaaaaababbbbaaaabaaabbabbbbbbbbabbaaaaaaabbbbbabaaabbbbbab
        aaaabbababaababbbababbaaaaaababbaaabaabbbaabaababbabaaabbaaabbbbbbbbabbaaaababababbaabbabbababbbaabb
        abaaaaabaaabaaaaaababbbbabbaaaaaababbabbbbabbaaabbaaabbbabababbabaaabbaabbbabaabbbababbbbbababbbaabb
        aaaababaabaabaabaaaaabaabababbabaabbbbaaabbababbabbbabbaabbaaababbbabbaaaabbbbabbaaabaabbbbaabbbabbb
        aaabaababbabaabaaabbbabbaabaaaabbaaaaabbaabbaabababaabbabbaabbbaabbababbabbbabababaabbbbbbababaabbab
        aaaaabaabaaabbababaaabababbbbaababaaabbabaaabaaabaabbaababbabbbabbbaababbabbbaabbbbababbabababbaabbb
        aaaaabbbbbaababaaabaaaabbaaabbbabbabbbaaabaaabbaabbbaabbabbbaaabaabaabaaaaabbbabbbabbbbbbaaaaabbbbbb
        abaaaaababaaaaaaabaaabbabbabbbaabbabbbababbaaaabbbbbbabaabbbbababbaaaaabbbabaaabbabaabbbbaababbabbab
        abaabbabaaaaabbbababbaabaaabbababababaabababababbbbbaabbaaabbbaaabaaaaaababbaaabaabbabbbbabaabbbbbbb
        abaaaabbaabbabbaaaabaabbaabbbaababaabababbaabaaaaabaabaaaabbabbbbaababbbabbabbbbbaabbbaabababbbbabab
        aabaabbababbaaaaabbaabaaabaabababbbbbbbaaabaaabbbaaaabaabababbabbababbbbaaabbbbbaaabbaabbaaabbbabbab
        aaaababaabbaabbbababbaaabbbabaababaaaabbbaabaaabbaabbaabababaabababbbbabbbaabbaabaaabbabaabaabbbbbbb
        aaaaaaabbaababaabbbabaabaaaababbbaaabbbbabaabbbbaabbbaabaabbbbaabababbaabbabaabbaaabaabbbaabbbbababb
        aaabaaaaaaabbbbaaabababaaaabbabbbbbaaaabbbbaaababaaaaabaaaabababbaaabaabbbbaaabbbbbbabbbabbbbbbabbbb
        aaaaabababbbbbaaaaabaabbaaaaaabbabbbabbaaabaaaaaabbbbaabaabbbbbababbbbbaaababbbbababbbaabbaabaababbb
        abaaabaaaaababbbaaaaabbabaaaaaaababbaaabaaabbbbbababaabbbabaabbabbababaaabbbbababbbbbbbbbababaabbbab
        aaaabaaabbaabbbbbaaabbaaabbaabbbbbaaaaaaabbaaabbbaaaaaabababbbbbabaaabbbaaaabbbaabbbbababbbbababbbab
        aabaabaabaaabaaabbbaabaabbbbabbabbabaaaababbbabbbaaabbaabaababbaaaababbbabaaababbabababbbabbbaaabbbb
        abaababbaaaaabaaaabbababbabbbbaaabbbabaabbbaabbabaababababaabbbaaabaabababaaaabbababbbbbbaaabbbabbab
        abaabbaaabaabbabaababaabaabbbbaaaaaabbbbaaaabbaabbaaabababababbabbbbbabbaabbbbaababaabbabbabaaaabbbb
        aaaabbaabaaaabbbaaababaaabbbbbabaaabaaabaabaaababbbbbabbbbababbaaabbbabbbbababaaabaababababbbabaabbb
        aaaaaaaaaaabbaaabbaababbbaabbbbbbbbaaaabaaaaabbbaabbabbaabababaaaababbbbbbbbbbbbaabaaaabbbbaaaabbbbb
        aaabbabbababaaaaaaaaababbaaaabbbbabaabbaabbbbaabaababbbaabaabbbbbabbabbbaaabbbaababbaaaabbaababbbbab
        aaaaaabaabaaabbaaaababaaabbbbababbabbabbbaabbaababbbabaabbaabbabbbbbaaababababbabbaaabbbabaabababbab
        abaaabaaabaaabbaaababaaabaabaabaaabaaaabbabbbaaabbbabbbbbababbabbbbaabbaabbaaabbbbbbbabbaaaaabbbbbab
        aaaabbaabbbaabaaabaabbaaabbabaaababaaaaabbabbbaabaaabaabbaabbababaabababbbaabbbbabbabaaabbbbbabbbbbb
        aabaaabbaaababaaabbbaaaaaabbaaaabbababbaabbbbbabababbaabaaaabbaaabbbbbbbabaabbbbaaabbbabbabababababb
        abaaaababbabbbababaaababaabbaaababbaabaaabaaaaaabbbabbbbbbaabaaaabbaabbbaaabbbbabbbbababbaabbabbaabb
        aabaaabbbaaaabababaaabbbbabbbaaaababaaababbbaaabbabbbaabbabaaaaabbbbbabbababbaaabbaabaaabbbbabbbaabb
        aaaaaabaaabbabbabbbbabaaababaababaababbbbbbabbabaaabbbaabaabaaaaaabbbbbaabbbbabaababbababbabaababbab
        abaaabbaabbaaaabbbbbabababaaaaababbabaabaabbaaaaabbababbaaaabaabbabbabbabababbbbbababbababbabaabbbab
        aabaaaaaaaabaabaaababbaabbbaababbabababbbabbbabbbaaabbabaaabbaaababbbbaabbaabbabbbbaaabababbbaaabbbb
        abaaaaaaaaababbbabbabbbabaaabbababbaababbbaabbbaaaabaaabbabaaabaabbabbbbaaaaababbabbbbbabababbbaabbb
        aabbababaaababbaabaaababbabababbaaaaabbbbbaaaabbbabaabbbabaaabbaabbabbabbababbaababaaabbbabaaabbabbb
        abaaaaaaaabaabbabbabbbaabaababbbbaabababbaaaabaababababbaabaaababbbaaabbbabbbaabbaabbababbbabbabbabb
        aababaaaababaabbabaaabaaaababaabbabbaabaababbaabbabbbbbabababaaabbabbbbbbababbaabaababaababbbabaabbb
        aaababbaaabbabbaaaabbaabaaabaaabbaaaaaaaaabaabbabbbaabbbbbabbbababbabbbbabbabaaaaabbaabbbbbaaabbbbbb
        aaababaabaaaaaabbbbbbababaaaababbbbaabababbabaabaabbaaabbaaaabbbaabbbaaabbaabbbaaabbbbbbaabbbabbaabb
        aaabaabaaaaaabaabbbbbbbbaaabbabbbaabaabaabaaabaabbabbaaaabaaabaababbbbabbbaabbaababbbaababbbababbbbb
        aabbaaaabbaaabbaabbabaabbabbabaaabbabaaabbababbaaaaababbbbbbabaaabbbaabbaaabbbbaaaababbbbabbababaabb
        abababaabaababaaaaabbabbabbababbabaaaabaababbbbaaaababbbbbbaabbaaababbaaaabaaaaabbabbbbabbbbaababbbb
        ababaaaabaabbaaaabbabaaaababbabababaaaaaaabaabaababbbbabbbbbbabbabaaabbabbbbababbaaaabbbbaabbbabbabb
        aaababaabaaababbabbbabaabaabaabaabaabaaaabbabbbaabbaaaaaabaabbbbbabbbababbbabbbbbbaaaabbbabababbabab
        aaaaaaabbbbbaaabbaaaababaaaaaabbaabbabbbbbbbaaaaaaababbaabbaaababbbabbabababbaabaabbabbbabbababbbbbb
        aaaababbabbaabbabbabaabbabaaababaaabaaababbabbabaaaaaaabbbaababbbabbbbbbababaabbabaaabaababaabbbbbbb
        aaabaababbaaaabaaabbbabaabaabaaabaababbbbbbbabbabbbaabbbaaabaaababbaaababbbbbabbabaaaaaabbababbabbbb
        abaabbaaabaabbabbabaabaaabaabaaabbbbbbabaabbaaaabbabaabbaaaabaabababbaabbbababbbbbbbaabaaabbaaabbbbb
        abaababaaaaaaabbaabbabbababababbbbaabaaaababaaabbbabbaaababbabbaabbabbabbaaabbabababbaabbbababbabbab
        aaaabaaabbabbbaabaaababbaabababbbaaaaabbbababbaaaaaaababbababbbaabaaabbaabbbbbbbbbabaaaabbbbaababbbb
        aaaaabababbaaabbbbaabaaaaababbbaababaabbaabaabbbbaaabbabbbaabaabbbbbabbbaaaabaaaababbababbaabbbbbabb
        aaaabababbaabbbabbabaaabaabbaaabaabbbbaaababaabbabbbbabbaaaabaabababababbabaaaababaaabbbbaabbbbbbbab
        aabbabaaabbaabbaaaabbbbabaababbaaababbbbababaabaabaaaaaabbbaaabbaababbbabbbbabbaaaaabaabbabbbbbbaabb
        aaaaabaaababaaaabbbaaaaaababaabababbabbababbbabbababbababbbbbababaababbbbababaaabaabbababbabbabbabab
        aabaabaabaabbbaabaabbbaaaaabaaaabbaaaaaabababbbababaabbababbbbbbbbbbabaabbaababaabbaababbbaaabbbbabb
        aabaababbabababababbabaaabaabbaababaababaaaabbbabbbabbabaabbbbaabaabbaaabbbabaaabbbaabbababbaaabbabb
        aabaababaabbbaabbaaabaabaabaaabbaabbaaaabbbbbaabbbaaababbbaabbbaaababbaaabbbbbbaaaababaabbabbbabbbab
        aaaaabbbaaababbaababbbaaabbababbabababbaabaabbabbbababaabababaabaaaabbaababbbbaabaaaabbbaabbababbbbb
        aaababababbaaaaaabaabaaaababaaababaabbaabbbbbaaabaabaaabbbbabbbababbabbbabbabbabbabbbaabbaaabbaabbbb
        aabbabaabaabaabaaaabbbbbaaabbaababbabaabbabaabaaaaaabbabaabaabbaabaabbbbbababbbbabaabababbbbbbababab
        aaaabbbbaabaaaaaaabbaaaaabaaaaabababbbabbbabbbababaaabbbbbbabbaaaaababbbbabaabbbababbbbabaaaabbabbbb
        aabbaaabbbabaaabaaababbabbbababaabababbaabbaaaababbbbbaaaabbbaabaabaababaaabbbbbbbabababaaaabbabbbab
        aabaaaaabbbbaaaabbbbbaabbbababaabaabaabbabababaaababaababbbbaaaabaaaaabbabaababaababbbbbaabbbabbbbbb
        aaaaabbbabbaaabaaaabbbbaaaababbbababbaaaaabaabaabababababbbaaaabbbbbbbbaaaabbaaaaabbbbbbababbbbbabab
        abaabaaaabbaaaabaabaaaabbbbaaaababbbbbbababbaabbaaabaabbbbaaabbabbbaaaaabbbbaababbbbbabababbabaabbab
        aaabaabaaaabbabaababaabbbbabaaabbaabbbaabaabbabbbaababaabbababbbabaaababbbbabaaaabbbaaabbabbababbbab
        aabaaaababbbababbababaababaaabaaabaaabbbabbabaaaaabbbbbabbbbaabbbaaabbbaaababbbaaabbbababbaabaaabbbb
        aabaabaaabaaaaababaabbbaabbabbbbbabaabaabbbaaaaabbababaaabbabaababbabaaabbbbabbbabaabbaaabbbbbabbabb
        aaabaaaaabbabaababbbaabaaabaaabbaaaababbaabbbbbbbbbaaabaabaaababbabababaababababbbbbbbbabaabaabbbbab
        abaaaaaaaaaabaabaaaababbaababbbbbbbbabbbbbbabaabbaabaabaaabbaaabababbabaaabaabaabbabbbbababbabbbbbab
        aabbababaabaabbaaabbabbaaabaabababbbaaaaaababbbabbaaaabaaaaabbbbbbbabaabbabbabbbbbaaaaabbbbabaabbabb
        aaabaaababaaabaababbabbabbaaabbababbbabbaaabaababaabbaaabbaabbabbbaabbaaabababbabababaabbbbbabbababb
        aaaaaaabbaabbaababaaaabbbbaabababbaabbaabbbbaabbabaaababaabbbababaabaaabbbbbaabbabaabbbaabbaababbbbb
        abaabababaababbaaababbbbaabaabaabaaabbbaaababaabbaabbbabbaabbabbbabaaabaabbaaabbbabbbaabbabaabbbaabb
        aaaaaaaaaabababbababbaabbaabbbababbbaabbbaabbbbaaaabbbbaabaabbaaaabaaabbababababaabaabababbbbbabbbbb
        aaaabababbabaaaabbabbaaaaabbabbbaababaabbbbaaaaabbabbbbbbaaabbaaabbaababbabbbbaaababbbabaaaabbbabbab
        aaaaabbaaaababbaabbaaabababbbaaabbbbabbababaaaabaaabbbbabbaabbaabbbabaabbaababaabbaababbabbbaaabbbbb
        aabaaaabbaabbabbaabababaabaabbbababbabbbaaabaaabaababbbaaababbaaaabaababababbababababbbababaabbbbbbb
        aabbabaaaaababbaaaabaaaabbbbbaaabaaaabaabbbaaabaaabababbaaabbbbbbaababaabbbabaabbbbbabbbbbabbbabaabb
        abaaaabbbaababbbaaaaaabbaabaabbbaaabaabbaaabababbabbbabbbaaaaabbababababaababababbabbbabbabbbabaabbb
    ''').strip().split('\n'))

    words_negative = map(str.strip, ('''
        bbbbbaabbbabbabaaababbbbabaaababbbbabaaaaababbbbbbbbaabbabaabbbabaabababbababbbaababbbaaaabbaaaabaab
        ababbaaababaabbaababbbbaaaabbabababbaabbbaabbaaaabaaaaaababbaabbaaababbaabbbabbaabbbbababaaabaaabaaa
        aabbabbbbbaabbbaabbabbbaaaaabbbbbaaaaaaabbbaaaababbabbaaabbabbbbbabbbbaaabbabbbababaabbabaabbbabbbaa
        abbabaaaaaaababbbbbbbabbabababbababababbbabbabaaaababaaaaabaabaabbaaaaaaaababbbbabbaabbbbbbbaaabaabb
        bbbaaaabaabbabababbbababbabaabaabbbabaaaababbaaaabbababaabbbbaaabaabbbbbaabaaababaabaabbaaabbbbbbbaa
        babbaaaababaaababbbaaabbaabbbaabbaaababbabaabbbbaaaaabbabbaaaabaaabbabbaaababbbbbbbabaababbaaabaaaaa
        bbbabababbbbbbbbaabaabaabababbbbbabbabbabaaababaaabaaabbbabaabbabbabaaabaabaaababbaaababbaaaaababbaa
        babbabaaaabaabbbabaabaaabbaaaaaabaababbbbaabbbabaababbaaabababbbbabbabbabbbbabbbbbbbababbbabaabbabaa
        aababaaaaabababbbbaabbaabbbabbbaabbbabbabbaaaaabbaabaababbabaabababbaabbbbaababaaaaabababbaaaabbabab
        aababbbbbbabbbbabaaabaabbabaabbabaaaabaababaaabbbaaaaaaaabaabbbbaaabbbbbabaabaabbabbaabbbaababbababa
    ''').strip().split('\n'))

    assert all(map(parser.predict, words_positive))
    assert not any(map(parser.predict, words_negative))

def test_all():
    parser = Earley()
    parser.fit(
        'S',
        'abcd',
        (
            ('S', 'aS'),
            ('S', 'bS'),
            ('S', 'cS'),
            ('S', 'dS'),
            ('S', '')
        ),
        'S'
    )

    words_positive = map(str.strip, ('''
        dcabacbaaadcaddcccdbaddadcdbbbdbaddbdaadbadddcbadcdbdaaaccdabdbbdbcbbccdccbcddbcbbdcdddbbdcbbcabdbdb
        badccbdaddabddbabbacdababbaddbdacabbddadcdddaccacccbcbababbbbbabbdbbbbbbbadabbcbdbabcccdbbbbadbbbaca
        addcadccdbbccadbdbaacbbcbbdbccacdcbcadadddacacdcbdbbabdbcbbdaaacacaddcacdadbccbdbaaccbbdcaabcdabcadb
        bacababccdadcccbcaacbdabacadbabdadcdbccaadbdcabcbabdaaadadccbaccdbbbacccbabddcbbcbbdcabbcddbcbdaacda
        cddcdcacbcddadadabcbcabbddbdaddabacabdbcccaadbcbabcdcadcdbabcddccdcacbbabaddbacbcbcdadbadcbccdddcbad
        acaddbccdabdaccadbccbbcdcdabbcadbcadcadbbabcccbacccaaddcbbbcaacdadcdadcddaccbabdacdadacccdcdaaccbbba
        adcabacbdbbacdadadbccbcaddbadcbaaabcaddaadbcadadbcddccadadabdbbadaccdcbacdbdbcdbcddbccaadaadbcacccca
        bddcdbcbaacadbcddcaaaaaacababddaccbdaacbbabdddbdcccccdcbdbcbccbadaaaaccbbcdaadcbdacaddbbbdbdcdccdcba
        aaadadacadcaadaabbbbccbaaabdaabadcaaadbdaacdcbacbaaaacdcbdbdbccccdbdaabcbdadbbddcababbbbbaddbdabdcdd
        dbbddaaaadbcbaabacacaadaadbadadbdacdbcabddcccbdaacdbccadabdadcdbbdbbbdcccdaadcbabcbaddbabdcadddddbac
    ''').strip().split('\n'))

    assert all(map(parser.predict, words_positive))

def test_none():
    parser = Earley()
    parser.fit(
        'ST',
        'abcd',
        (
            ('S', 'aS'),
            ('S', 'bS'),
            ('S', 'cS'),
            ('S', 'dS'),
            ('S', '')
        ),
        'T'
    )

    words_negative = map(str.strip, ('''
        dcabacbaaadcaddcccdbaddadcdbbbdbaddbdaadbadddcbadcdbdaaaccdabdbbdbcbbccdccbcddbcbbdcdddbbdcbbcabdbdb
        badccbdaddabddbabbacdababbaddbdacabbddadcdddaccacccbcbababbbbbabbdbbbbbbbadabbcbdbabcccdbbbbadbbbaca
        addcadccdbbccadbdbaacbbcbbdbccacdcbcadadddacacdcbdbbabdbcbbdaaacacaddcacdadbccbdbaaccbbdcaabcdabcadb
        bacababccdadcccbcaacbdabacadbabdadcdbccaadbdcabcbabdaaadadccbaccdbbbacccbabddcbbcbbdcabbcddbcbdaacda
        cddcdcacbcddadadabcbcabbddbdaddabacabdbcccaadbcbabcdcadcdbabcddccdcacbbabaddbacbcbcdadbadcbccdddcbad
        acaddbccdabdaccadbccbbcdcdabbcadbcadcadbbabcccbacccaaddcbbbcaacdadcdadcddaccbabdacdadacccdcdaaccbbba
        adcabacbdbbacdadadbccbcaddbadcbaaabcaddaadbcadadbcddccadadabdbbadaccdcbacdbdbcdbcddbccaadaadbcacccca
        bddcdbcbaacadbcddcaaaaaacababddaccbdaacbbabdddbdcccccdcbdbcbccbadaaaaccbbcdaadcbdacaddbbbdbdcdccdcba
        aaadadacadcaadaabbbbccbaaabdaabadcaaadbdaacdcbacbaaaacdcbdbdbccccdbdaabcbdadbbddcababbbbbaddbdabdcdd
        dbbddaaaadbcbaabacacaadaadbadadbdacdbcabddcccbdaacdbccadabdadcdbbdbbbdcccdaadcbabcbaddbabdcadddddbac
    ''').strip().split('\n'))

    assert not any(map(parser.predict, words_negative))

def test_empty():
    parser = Earley()
    parser.fit(
        'S',
        'abcd',
        (),
        'S'
    )

    words_negative = map(str.strip, ('''
        dcabacbaaadcaddcccdbaddadcdbbbdbaddbdaadbadddcbadcdbdaaaccdabdbbdbcbbccdccbcddbcbbdcdddbbdcbbcabdbdb
        
        badccbdaddabddbabbacdababbaddbdacabbddadcdddaccacccbcbababbbbbabbdbbbbbbbadabbcbdbabcccdbbbbadbbbaca
        addcadccdbbccadbdbaacbbcbbdbccacdcbcadadddacacdcbdbbabdbcbbdaaacacaddcacdadbccbdbaaccbbdcaabcdabcadb
        bacababccdadcccbcaacbdabacadbabdadcdbccaadbdcabcbabdaaadadccbaccdbbbacccbabddcbbcbbdcabbcddbcbdaacda
        cddcdcacbcddadadabcbcabbddbdaddabacabdbcccaadbcbabcdcadcdbabcddccdcacbbabaddbacbcbcdadbadcbccdddcbad
        acaddbccdabdaccadbccbbcdcdabbcadbcadcadbbabcccbacccaaddcbbbcaacdadcdadcddaccbabdacdadacccdcdaaccbbba
        adcabacbdbbacdadadbccbcaddbadcbaaabcaddaadbcadadbcddccadadabdbbadaccdcbacdbdbcdbcddbccaadaadbcacccca
        bddcdbcbaacadbcddcaaaaaacababddaccbdaacbbabdddbdcccccdcbdbcbccbadaaaaccbbcdaadcbdacaddbbbdbdcdccdcba
        aaadadacadcaadaabbbbccbaaabdaabadcaaadbdaacdcbacbaaaacdcbdbdbccccdbdaabcbdadbbddcababbbbbaddbdabdcdd
        dbbddaaaadbcbaabacacaadaadbadadbdacdbcabddcccbdaacdbccadabdadcdbbdbbbdcccdaadcbabcbaddbabdcadddddbac
    ''').strip().split('\n'))

    assert not any(map(parser.predict, words_negative))
