import sys

from earley import Earley
from lr1 import LR1


USED_PARSER = LR1

def main(istream):
    non_term_num, term_num, rules_num = map(int, istream().split())

    non_term = istream().strip()
    assert len(non_term) == non_term_num

    term = istream().strip()
    assert len(term) == term_num

    rules = []
    for _ in range(rules_num):
        rule_raw = istream()
        left, right = map(str.strip, rule_raw.split('->'))
        rules.append((left, right))

    start_symbol = istream().strip()

    parser = USED_PARSER()
    parser.fit(non_term, term, rules, start_symbol)

    words_num = int(istream())
    for _ in range(words_num):
        try:
            word = istream().strip()
        except EOFError:
            word = ''
        is_in_grammar = parser.predict(word)
        print('Yes' if is_in_grammar else 'No')

if __name__ == '__main__':
    if len(sys.argv) >= 3 and sys.argv[1] == '-f':
        file_name = sys.argv[2]
        with open(file_name, 'r') as f:
            main(f.readline)
    elif len(sys.argv) != 1:
        print('Usage: python3 main.py [-f <filename>]')
    else:
        main(input)
