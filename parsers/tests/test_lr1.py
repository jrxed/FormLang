import copy

import pytest

from lr1 import LR1


def test_basic():
    parser = LR1()
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


def test_balanced_bracket_sequence():
    parser = LR1()
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
    parser = LR1()
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
    parser = LR1()
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
    parser = LR1()
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


def test_not_lr1():
    parser = LR1()

    with pytest.raises(Exception):
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

    with pytest.raises(Exception):
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

    with pytest.raises(Exception):
        parser.fit(
            'SABC',
            'abcd',
            (
                ('S', 'CABC'),
                ('A', 'Aa'),
                ('B', 'Bb'),
                ('C', 'Cc'),
                ('A', ''),
                ('B', ''),
                ('C', '')
            ),
            'S'
        )
