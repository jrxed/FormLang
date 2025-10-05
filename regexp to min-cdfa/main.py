import json

from src.enfa import ENFA
from src.nfa import NFA
from src.dfa import DFA
from src.cdfa import CDFA
from src.mcdfa import MCDFA


def main():
    type_of_input = int(input('RegExp (0) / File with config (1): '))
    get_complement = int(input('Get an automaton (0) or its complement (1): '))
    assert type_of_input in (0, 1)
    assert get_complement in (0, 1)

    if type_of_input == 0:
        sigma = tuple(input('Enter alphabet (in one line without spaces): '))
        regexp = input('Enter RegExp: ')

        enfa = ENFA(regexp, sigma)
    else:
        with open('input.json') as f:
            config = json.load(f)
            config['sigma'] = list(config['sigma'])
            config['final'] = set(config['final'])

            enfa = ENFA(config)

    nfa = NFA(enfa)
    dfa = DFA(nfa)
    cdfa = CDFA(dfa)
    if get_complement == 1:
        cdfa.make_complementary()
    mcdfa = MCDFA(cdfa)

    automata = {
        'enfa': enfa,
        'nfa': nfa,
        'dfa': dfa,
        'cdfa': cdfa,
        'mcdfa': mcdfa
    }

    results = {}

    for automaton in automata.keys():
        cfg = automata[automaton].get_config()
        cfg['final'] = list(cfg['final'])
        results.setdefault(automaton, cfg)

    with open('output.json', 'w') as f:
        json.dump(results, f, indent=4)

if __name__ == '__main__':
    main()
