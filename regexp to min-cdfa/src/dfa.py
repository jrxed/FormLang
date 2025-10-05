from .nfa import NFA


class DFA(NFA):
    def __init__(self, *args):
        if len(args) == 1 and type(param := args[0]) == DFA:
            for key in self.config_keys:
                setattr(self, key, getattr(param, key))
        else:
            super().__init__(*args)
            self.determinise()

    def determinise(self):
        delta_dict = self.get_delta_dict()

        queue = [{self.start}]
        used_sets = set()
        transitions = {}

        while queue:
            new_queue = []
            for nodes_set in queue:
                nodes_frozen = frozenset(nodes_set)
                for char in self.sigma:
                    dest_nodes_set = set()
                    for node in nodes_set:
                        if not node in delta_dict.keys() or \
                            not char in delta_dict[node].keys():
                            continue
                        for dest_node in delta_dict[node][char]:
                            dest_nodes_set.add(dest_node)

                    if not dest_nodes_set:
                        continue

                    dest_nodes_frozen = frozenset(dest_nodes_set)
                    transitions.setdefault((nodes_frozen, char), dest_nodes_frozen)

                    if not dest_nodes_frozen in used_sets:
                        used_sets.add(dest_nodes_frozen)
                        new_queue.append(dest_nodes_frozen)

            queue = new_queue

        nodes_sets_indices = {}
        index = 0

        for key_set, char in transitions.keys():
            if not key_set in nodes_sets_indices.keys():
                nodes_sets_indices.setdefault(key_set, index)
                index += 1

            value_set = transitions[(key_set, char)]
            if not value_set in nodes_sets_indices.keys():
                nodes_sets_indices.setdefault(value_set, index)
                index += 1

        if not transitions:
            nodes_sets_indices.setdefault(frozenset({0}), 0)
            index += 1

        old_final_nodes_set = self.final.copy()

        self.start = 0
        self.states = [i for i in range(index)]
        self.final.clear()
        self.delta.clear()

        for key in nodes_sets_indices.keys():
            intersection = key.intersection(old_final_nodes_set)
            if intersection:
                self.final.add(nodes_sets_indices[key])

        for key in transitions.keys():
            source_nodes_set = key[0]
            sym = key[1]
            dest_nodes_set = transitions[key]

            source_node = nodes_sets_indices[source_nodes_set]
            dest_node = nodes_sets_indices[dest_nodes_set]

            self.delta.append({
                'from': source_node,
                'to': dest_node,
                'sym': sym
            })
