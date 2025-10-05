from .reg import RegExp


class AST:
    class Node:
        def __init__(self, string):
            self.char = None
            self.children = []
            self.build(string)

        def add_child(self, node):
            self.children.append(node)

        def get_char(self):
            return self.char

        def get_children(self):
            return self.children

        def build(self, regexp):
            assert len(regexp) != 0
            if len(regexp) == 1:
                self.char = regexp
                return

            curr_balance = 0

            for pos, char in enumerate(regexp):
                if char == '(':
                    curr_balance += 1
                elif char == ')':
                    curr_balance -= 1

                if curr_balance == 0:
                    if pos + 1 < len(regexp):
                        if regexp[pos + 1] == '|':
                            self.char = '|'
                            self.add_child(AST.Node(regexp[:pos + 1]))
                            self.add_child(AST.Node(regexp[pos + 2:]))
                            return

                        elif regexp[pos + 1] in '*+':
                            if pos != len(regexp) - 2:
                                self.char = '.'
                                self.add_child(AST.Node(regexp[:pos + 2]))
                                self.add_child(AST.Node(regexp[pos + 2:]))
                                return

                            substr = regexp[1:-2]
                            if regexp[pos + 1] == '+':
                                self.char = '.'
                                self.add_child(AST.Node(substr))
                                self.add_child(AST.Node('(' + substr + ')*'))
                                return

                            self.char = '*'
                            self.add_child(AST.Node(substr))
                            return
                        else:
                            self.char = '.'
                            self.add_child(AST.Node(regexp[:pos + 1]))
                            self.add_child(AST.Node(regexp[pos + 1:]))
                            return

            assert regexp[0] == '(' and regexp[-1] == ')'
            self.build(regexp[1:-1])
            return


    def __init__(self, string, sigma):
        regexp = RegExp(string, sigma)
        self.regexp = regexp.get_string()
        self.sigma = sigma
        self.root = self.Node(self.regexp)

    def get_root(self):
        return self.root

    def get_sigma(self):
        return self.sigma
