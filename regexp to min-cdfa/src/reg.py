class RegExp:
    def __init__(self, string, sigma):
        assert sigma
        self.sigma = tuple(sorted(sigma))
        self.string = string

        self.add_parentheses()
        self.add_parentheses(reverse=True)

    def reverse_string(self):
        new_string = ''

        for char in self.string[::-1]:
            if char == '(':
                new_string += ')'
            elif char == ')':
                new_string += '('
            else:
                new_string += char

        self.string = new_string

    def add_parentheses(self, reverse=False):
        if reverse:
            self.reverse_string()

        while True:
            balance = [0 for _ in range(len(self.string) + 1)]
            curr_balance = 0

            for pos, char in enumerate(self.string):
                if char == '(':
                    curr_balance += 1
                elif char == ')':
                    curr_balance -= 1
                elif char in ('+*|' if not reverse else '|'):
                    if self.string[pos - 1] != ')':
                        if char in '+*' and not self.string[pos - 1] in '+*':
                            self.string = self.string[:pos - 1] + '(' + self.string[pos - 1] + ')' + self.string[pos:]
                            break
                        index = pos - 1
                        while balance[index] != curr_balance - 1 and index > 0:
                            index -= 1
                        self.string = self.string[:index] + '(' + self.string[index:pos] + ')' + self.string[pos:]
                        break
                balance[pos + 1] = curr_balance
            else:
                break

        if reverse:
            self.reverse_string()

    def get_string(self):
        return self.string

    def get_sigma(self):
        return self.sigma
