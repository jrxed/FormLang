from .astree import AST


class ENFA:
    config_keys = ['sigma', 'start', 'states', 'final', 'delta']

    def __init__(self, *args):
        self.sigma = None
        self.start = None
        self.states = None
        self.final = None
        self.delta = None

        assert len(args) <= 2
        if not args:
            return

        param = args[0]

        if type(param) == dict:
            assert len(args) == 1
            self.set_config(param)
        elif type(param) == ENFA:
            assert len(args) == 1
            for key in self.config_keys:
                setattr(self, key, getattr(param, key))
        elif type(param) == str:
            assert len(args) == 2
            self.sigma = args[1]
            self.build(param)
        elif type(param) == tuple:
            assert len(args) == 1
            self.sigma = param

    def get_config(self):
        return {key: getattr(self, key) for key in self.config_keys}

    def set_config(self, config):
        for key in config.keys():
            setattr(self, key, config[key])

    def get_delta_dict(self):
        delta_dict = {}

        for mapping in self.delta:
            source = mapping['from']
            dest = mapping['to']
            sym = mapping['sym']

            if source not in delta_dict.keys():
                delta_dict[source] = {}
            if sym not in delta_dict[source].keys():
                delta_dict[source][sym] = []

            delta_dict[source][sym].append(dest)

        return delta_dict

    def build(self, string):
        ast = AST(string, self.sigma)

        self.set_config(self.build_from_ast(ast.get_root()).get_config())
        self.sigma = ast.get_sigma()

    def build_from_ast(self, node):
        char = node.get_char()

        automata = [self.build_from_ast(child) for child in node.get_children()]

        if not automata:
            assert char
            config = {
                'sigma': self.sigma,
                'start': 0,
                'states': [0, 1],
                'final': {1},
                'delta': [{
                    'from': 0,
                    'to': 1,
                    'sym': char if not char in ('1', 'ε') else ''
                }]
            }
            result = ENFA(config)
            return result
        elif len(automata) == 1:
            assert char == '*'
            result = ENFA(automata[0])

            for state in result.final:
                result.delta.append({
                    'from': state,
                    'to': result.start,
                    'sym': '',
                })
                result.final = {result.start}
                return result

        assert len(automata) == 2

        if char == '.':
            result = ENFA(automata[0])
            size_first = len(result.states)
            result.states.extend([state + size_first for state in automata[1].states])
            result.final = {state + size_first for state in automata[1].final}
            result.delta.extend([{
                'from': transition['from'] + size_first,
                'to': transition['to'] + size_first,
                'sym': transition['sym']
            } for transition in automata[1].delta])
            result.delta.extend([{
                'from': state,
                'to': automata[1].start + size_first,
                'sym': ''
            } for state in automata[0].final])
            return result

        assert char == '|'
        result = ENFA()
        result.start = 0
        result.final = {1}
        size_first = len(automata[0].states)
        result.states = [0, 1] + [state + 2 for state in automata[0].states] + \
            [state + size_first + 2 for state in automata[1].states]
        result.delta = [{
            'from': transition['from'] + 2,
            'to': transition['to'] + 2,
            'sym': transition['sym']
        } for transition in automata[0].delta] + [{
            'from': transition['from'] + size_first + 2,
            'to': transition['to'] + size_first + 2,
            'sym': transition['sym']
        } for transition in automata[1].delta] + [{
            'from': 0,
            'to': automata[0].start + 2,
            'sym': ''
        }] + [{
            'from': 0,
            'to': automata[1].start + size_first + 2,
            'sym': ''
        }] + [{
            'from': state + 2,
            'to': 1,
            'sym': ''
        } for state in automata[0].final] + [{
            'from': state + size_first + 2,
            'to': 1,
            'sym': ''
        } for state in automata[1].final]

        return result

    def fix_numeration(self):
        new_states = [i for i in range(len(self.states))]
        old_to_new = [0 for _ in range(max(self.states) + 1)]
        new_final = set()
        new_delta = []

        for new, old in enumerate(self.states):
            old_to_new[old] = new
            if old in self.final:
                new_final.add(new)

        for transition in self.delta:
            new_delta.append({
                'from': old_to_new[transition['from']],
                'to': old_to_new[transition['to']],
                'sym': transition['sym']
            })

        self.start = 0
        self.states = new_states
        self.final = new_final
        self.delta = new_delta
