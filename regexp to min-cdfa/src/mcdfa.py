from .cdfa import CDFA


class MCDFA(CDFA):
    def __init__(self, *args):
        if len(args) == 1 and type(param := args[0]) == MCDFA:
            for key in self.config_keys:
                setattr(self, key, getattr(param, key))
        else:
            super().__init__(*args)
            self.minimize()

    def minimize(self):
        delta_dict = self.get_delta_dict()
        size = len(self.states)
        table = [[0 for _ in range(size)] for _ in range(len(self.sigma) + 1)]

        for state in self.states:
            table[0][state] = 1 if state in self.final else 0

        copy = None
        eq_classes = {}

        end_states = table[0].copy()

        while table[0] != copy:
            eq_classes.clear()
            eq_class_index = 0
            copy = table[0].copy()
            states_eq_classes = [0 for _ in range(size)]

            for state in self.states:
                for char_index, char in enumerate(self.sigma):
                    assert len(delta_dict[state][char]) == 1
                    dest_state = delta_dict[state][char][0]
                    dest_class = table[0][dest_state]
                    table[char_index + 1][state] = dest_class

                state_info = tuple([table[i][state] for i in range(len(self.sigma) + 1)])
                if state_info not in eq_classes:
                    eq_classes.setdefault(state_info, eq_class_index)
                    eq_class_index += 1

                states_eq_classes[state] = eq_classes[state_info]

            table[0] = states_eq_classes.copy()


        self.start = 0
        self.states.clear()
        self.final.clear()
        self.delta.clear()

        last_index = -1
        for index in range(size):
            eq_class = table[0][index]
            if last_index < eq_class:
                last_index = eq_class

                self.states.append(last_index)
                if end_states[index]:
                    self.final.add(last_index)
                for char_index, char in enumerate(self.sigma):
                    self.delta.append({
                        'from': last_index,
                        'to': table[char_index + 1][index],
                        'sym': char
                    })
