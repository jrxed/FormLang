class LR1:
    MOCK_SYMBOL = '$'
    END_RULE_SYMBOL = '#'

    class State:
        def __init__(self, head, body, dot_index, next_term):
            self.head = head
            self.body = body
            self.dot_index = dot_index
            self.next_term = next_term

        def __repr__(self):
            body_with_dot = self.body[:self.dot_index] + '*' + self.body[self.dot_index:-1]
            return f'({self.head} -> {body_with_dot}, {self.next_term})'

        def __eq__(self, other):
            return (self.head, self.body, self.dot_index, self.next_term) == \
                   (other.head, other.body, other.dot_index, self.next_term)

        def __hash__(self):
            return hash((self.head, self.body, self.dot_index, self.next_term))

        @property
        def next_char_inside(self):
            return self.body[self.dot_index]

        @property
        def second_next_char_inside(self):
            return self.body[self.dot_index + 1]

        @property
        def len(self):
            return len(self.body) - 1

    def __init__(self):
        self.non_terms = ''
        self.terms = ''
        self.productions = {}
        self.closures = {}
        self.jumps = []
        self.table = []
        self.first = {}
        self.all_states = {}
        self.giving_eps = ''

    def __find_giving_eps(self):
        changed = True
        while changed:
            changed = False

            for head in self.productions.keys():
                if head in self.giving_eps:
                    continue
                for body in self.productions[head]:
                    for char in body:
                        if char in self.terms:
                            break
                        if char in self.non_terms and not char in self.giving_eps:
                            break
                    else:
                        self.giving_eps += head

    def __init_first(self):
        for term in self.terms:
            self.first.setdefault(term, {term})

        for non_term in self.non_terms:
            head_first_any = {non_term}

            changed = True
            while changed:
                old_size = len(head_first_any)

                for head in head_first_any.copy():
                    if head in self.productions.keys():
                        possible = set()
                        for body in self.productions[head]:
                            for char in body:
                                possible.add(char)
                                if char not in self.giving_eps:
                                    break
                        head_first_any = head_first_any.union(possible)

                changed = old_size != len(head_first_any)

            self.first.setdefault(non_term, set(filter(lambda c: c not in self.non_terms, head_first_any)))

    def __make_closure(self, closure):
        new_closure = closure.copy()
        return_index = len(self.closures)

        changed = True
        while changed:
            old_size = len(new_closure)

            for state in new_closure.copy():
                head = state.next_char_inside
                if head in self.productions.keys():
                    for body in self.productions[head]:
                        if state.second_next_char_inside == self.END_RULE_SYMBOL:
                            possible_next_term = {state.next_term}
                        else:
                            copy = self.State(state.head, state.body, state.dot_index, state.next_term)
                            second_next = copy.second_next_char_inside
                            possible_next_term = self.first[second_next]
                            while second_next in self.giving_eps:
                                possible_next_term = possible_next_term.union(self.first[second_next])
                                copy.dot_index += 1
                                second_next = copy.second_next_char_inside

                        for next_term in possible_next_term:
                            new_state = self.State(head, body, 0, next_term)
                            new_closure.add(new_state)

            changed = old_size != len(new_closure)

        if not new_closure:
            return -1

        for i in self.closures.keys():
            if self.closures[i] == new_closure:
                return i

        self.closures.setdefault(return_index, new_closure)

        new_closures = {}

        for state in new_closure:
            if not state in self.all_states.keys():
                self.all_states.setdefault(state, return_index)

            next_char = state.next_char_inside
            if next_char != self.END_RULE_SYMBOL:
                if not next_char in new_closures.keys():
                    new_closures.setdefault(next_char, set())

                copy = self.State(state.head, state.body, state.dot_index + 1, state.next_term)
                new_closures[next_char].add(copy)

        for char in new_closures.keys():
            inserted_index = self.__make_closure(new_closures[char])
            if inserted_index != -1:
                self.jumps.append((return_index, inserted_index, char))

        return return_index

    def __init_closures(self):
        start_closure = {
            self.State(self.MOCK_SYMBOL, self.productions[self.MOCK_SYMBOL][0], 0, self.END_RULE_SYMBOL)
        }

        self.__make_closure(start_closure)

    def __init_table(self):
        size = len(self.closures)

        self.table = [{key: 'Reject' for key in self.terms + self.non_terms + self.END_RULE_SYMBOL} for _ in range(size)]

        for dst, src, char in self.jumps:
            new_value = f'Shift {src}'
            if not self.table[dst][char] in ('Reject', new_value):
                # print(dst, src, char, self.table[dst][char], new_value)
                raise Exception('Incorrect grammar')

            self.table[dst][char] = new_value

        for index in self.closures.keys():
            closure = self.closures[index]
            for state in closure:
                if state.next_char_inside == self.END_RULE_SYMBOL:
                    next_term = state.next_term
                    new_value = f'Reduce {state.len} {state.head}' \
                        if state.head != self.MOCK_SYMBOL else 'Accept'

                    if not self.table[index][next_term] in ('Reject', new_value):
                        # print(index, next_term, self.table[index][next_term], new_value)
                        raise Exception('Incorrect grammar')

                    self.table[index][next_term] = new_value

        # print(self)

    def __fit_helper(self):
        self.__find_giving_eps()
        self.__init_first()
        self.__init_closures()
        self.__init_table()

    def fit(self, non_terms, terms, grammar, start_symbol):
        self.non_terms = non_terms
        self.terms = terms

        for head, body in grammar:
            if not head in self.productions.keys():
                self.productions[head] = []
            self.productions[head].append(body + self.END_RULE_SYMBOL)

        self.productions[self.MOCK_SYMBOL] = [start_symbol + self.END_RULE_SYMBOL]

        self.__fit_helper()

    def __repr__(self):
        print('FIRST:')
        for char in self.terms + self.non_terms:
            print(f'{char}: {self.first[char]}')

        print()
        print('Closures:')
        for index in sorted(self.closures.keys()):
            print(f'{index}: {self.closures[index]}')

        print()
        print('Table:')
        print(':) ', end = ' ')
        for char in self.terms + self.non_terms + self.END_RULE_SYMBOL:
            print(f'{char:<10}', end = ' ')

        for index in range(len(self.closures)):
            print()
            for char in ' ' + self.terms + self.non_terms + self.END_RULE_SYMBOL:
                if char == ' ':
                    print(f'{index:<3}', end = ' ')
                else:
                    x = self.table[index][char]
                    print(f'{x:<10}', end=' ')
        print()

        return ''

    def predict(self, word):
        word += self.END_RULE_SYMBOL
        # print(word)
        path = [0]
        current_closure = 0

        index = 0
        while index < len(word):
            char = word[index]
            instruction = self.table[current_closure][char]
            # print(path, '-> ', end='')
            while instruction.startswith('Reduce'):
                length = int(instruction.split()[1])
                char = instruction.split()[2]
                for _ in range(2 * length):
                    path.pop()

                # print(path)
                # print(path, '-> ', end='')

                current_closure = path[-1]
                instruction = self.table[current_closure][char]

            if instruction == 'Reject':
                return False

            if instruction == 'Accept':
                return True

            if instruction.startswith('Shift'):
                if char in self.terms:
                    index += 1

                next_closure = int(instruction.split()[1])
                path.append(char)
                path.append(next_closure)
                current_closure = next_closure
            # print(path)

        raise Exception('Something went wrong')
