class Earley:
    MOCK_SYMBOL = '$'
    END_RULE_SYMBOL = '#'

    class State:
        def __init__(self, head, body, i, j, dot_index):
            self.head = head
            self.body = body
            self.i = i
            self.j = j
            self.dot_index = dot_index

            self.is_completed = False
            self.is_predicted = False

        def __repr__(self):
            body_with_dot = self.body[:self.dot_index] + '*' + self.body[self.dot_index:-1]
            return f'({self.head} -> {body_with_dot}, {self.i}, {self.j})'

        def __eq__(self, other):
            return (self.head, self.body, self.i, self.j, self.dot_index) == \
                   (other.head, other.body, other.i, other.j, other.dot_index)

        def __hash__(self):
            return hash((self.head, self.body, self.i, self.j, self.dot_index))

        @property
        def next_char(self):
            return self.body[self.dot_index]

    def __init__(self):
        self.non_terms = ''
        self.terms = ''
        self.productions = {}

    def __scan_state(self, state, char):
        if state.next_char == char:
            return self.State(state.head, state.body, state.i, state.j + 1, state.dot_index + 1)

    def __predict_state(self, state):
        state.is_predicted = True
        new_states = []

        head = state.next_char
        if head in self.non_terms and head in self.productions.keys():
            for body in self.productions[head]:
                new_states.append(self.State(head, body, state.j, state.j, 0))

        return new_states

    def __complete_state(self, state_sets, state):
        state.is_completed = True
        if state.next_char != Earley.END_RULE_SYMBOL:
            return []

        new_states = []
        head = state.head

        for index in range(state.j + 1):
            if head not in state_sets[index]:
                continue

            for prev_state in state_sets[index][head]:
                if prev_state.j == state.i:
                    new_states.append(self.State(prev_state.head, prev_state.body, prev_state.i,
                                                   state.j, prev_state.dot_index + 1))

        return new_states

    def __scan_state_set(self, state_set, char):
        scanned_state_set = {}

        for _, state_arr in state_set.items():
            for state in state_arr:
                if scanned_state := self.__scan_state(state, char):
                    self.__add_state_to_state_set(scanned_state_set, scanned_state)

        return scanned_state_set

    def __predict_state_set(self, state_set):
        predicted_state_set = {}

        for _, state_arr in state_set.items():
            for state in state_arr:
                self.__add_state_to_state_set(predicted_state_set, state)
                if not state.is_predicted:
                    if predicted_states := self.__predict_state(state):
                        for predicted_state in predicted_states:
                            self.__add_state_to_state_set(predicted_state_set, predicted_state)

        previous_size = sum((len(arr) for arr in state_set.values()))
        new_size = sum((len(arr) for arr in predicted_state_set.values()))

        return previous_size != new_size, predicted_state_set

    def __complete_state_set(self, state_sets, state_set):
        completed_state_set = {}

        for _, state_arr in state_set.items():
            for state in state_arr:
                self.__add_state_to_state_set(completed_state_set, state)
                if not state.is_completed:
                    if completed_states := self.__complete_state(state_sets, state):
                        for completed_state in completed_states:
                            self.__add_state_to_state_set(completed_state_set, completed_state)

        previous_size = sum((len(arr) for arr in state_set.values()))
        new_size = sum((len(arr) for arr in completed_state_set.values()))

        return previous_size != new_size, completed_state_set

    @staticmethod
    def __add_state_to_state_set(state_set, state):
        head = state.next_char

        if not head in state_set.keys():
            state_set[head] = set()

        state_set[head].add(state)

    def fit(self, non_terms, terms, grammar, start_symbol):
        self.non_terms = non_terms
        self.terms = terms

        for head, body in grammar:
            if not head in self.productions.keys():
                self.productions[head] = []
            self.productions[head].append(body + self.END_RULE_SYMBOL)

        self.productions[self.MOCK_SYMBOL] = [start_symbol + self.END_RULE_SYMBOL]

    def predict(self, word):
        start_state = self.State(self.MOCK_SYMBOL, self.productions[self.MOCK_SYMBOL][0], 0, 0, 0)
        state_sets = [{start_state.body: {start_state}}]

        states_changed = True
        while states_changed:
            states_changed_after_predict, state_sets[0] = self.__predict_state_set(state_sets[0])
            states_changed_after_complete, state_sets[0] = self.__complete_state_set(state_sets, state_sets[0])

            states_changed = states_changed_after_predict or states_changed_after_complete

        for index, char in enumerate(word):
            state_sets.append(self.__scan_state_set(state_sets[index], char))

            states_changed = True
            while states_changed:
                states_changed_after_predict, state_sets[index + 1] = \
                    self.__predict_state_set(state_sets[index + 1])
                states_changed_after_complete, state_sets[index + 1] = \
                    self.__complete_state_set(state_sets, state_sets[index + 1])

                states_changed = states_changed_after_predict or states_changed_after_complete

        if not self.END_RULE_SYMBOL in state_sets[len(word)]:
            return False

        for state in state_sets[len(word)][self.END_RULE_SYMBOL]:
            if state.head == self.MOCK_SYMBOL:
                return True

        return False
