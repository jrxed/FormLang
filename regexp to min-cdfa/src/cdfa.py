from .dfa import DFA


class CDFA(DFA):
    def __init__(self, *args):
        if len(args) == 1 and type(param := args[0]) == CDFA:
            for key in self.config_keys:
                setattr(self, key, getattr(param, key))
        else:
            super().__init__(*args)
            self.make_complete()

    def make_complete(self):
        if len(self.delta) == len(self.sigma) * len(self.states):
            return

        extra_state = len(self.states)
        self.states.append(extra_state)

        delta_dict = self.get_delta_dict()

        for state in self.states:
            if state not in delta_dict.keys():
                for char in self.sigma:
                    self.delta.append({
                        'from': state,
                        'to': extra_state,
                        'sym': char
                    })
                continue
            for char in self.sigma:
                if char not in delta_dict[state].keys():
                    self.delta.append({
                        'from': state,
                        'to': extra_state,
                        'sym': char
                    })

    def make_complementary(self):
        self.final = set(self.states).difference(self.final)
