from .enfa import ENFA
from .details import compress_cycles, find_path


class NFA(ENFA):
    def __init__(self, *args):
        if len(args) == 1 and type(param := args[0]) == NFA:
            for key in self.config_keys:
                setattr(self, key, getattr(param, key))
        else:
            super().__init__(*args)
            self.remove_epsilon_transitions()

    def remove_epsilon_transitions(self):
        edges = {}
        for transition in self.delta:
            if transition['from'] != transition['to'] and transition['sym'] == '':
                if transition['from'] not in edges.keys():
                    edges.setdefault(transition['from'], set())
                edges[transition['from']].add(transition['to'])

        new_vertices = compress_cycles(self.states, edges)

        self.states = list(set(new_vertices))

        new_final = set()
        for old, new in enumerate(new_vertices):
            if old in self.final:
                new_final.add(new)
        self.final = new_final

        new_delta = []
        for transition in self.delta:
            source = transition['from']
            dest = transition['to']
            sym = transition['sym']

            new_transition = {
                'from': new_vertices[source],
                'to': new_vertices[dest],
                'sym': sym
            }

            if new_vertices[dest] == new_vertices[source] and sym == '':
                continue

            new_delta.append(new_transition)

        self.delta = new_delta

        self.fix_numeration()

        delta_dict = self.get_delta_dict()

        new_edges = {}
        for transition in self.delta:
            if transition['from'] != transition['to'] and transition['sym'] == '':
                if transition['from'] not in new_edges.keys():
                    new_edges.setdefault(transition['from'], set())
                new_edges[transition['from']].add(transition['to'])

        stack = find_path(self.states, new_edges)

        for source, dest in stack:
            if dest in self.final:
                self.final.add(source)

            if dest not in delta_dict.keys():
                continue
            transitions = delta_dict[dest]

            for char in transitions.keys():
                if char not in delta_dict[source].keys():
                    delta_dict[source].setdefault(char, [])

                delta_dict[source][char].extend(transitions[char])

        self.delta = []
        for source in delta_dict.keys():
            for char in delta_dict[source].keys():
                if char == '':
                    continue
                for dest in set(delta_dict[source][char]):
                    new_transition = {
                        'from': source,
                        'to': dest,
                        'sym': char
                    }
                    self.delta.append(new_transition)
