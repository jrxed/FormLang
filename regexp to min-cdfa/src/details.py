def compress_cycles_dfs(v, vertices, edges, colors, cycle):
    colors[v] = 1

    if v in edges.keys():
        for u in edges[v]:
            if colors[u] == 1:
                cycle.append(u)
                cycle.append(v)
                return u
            elif colors[u] == 0:
                res = compress_cycles_dfs(u, vertices, edges, colors, cycle)
                if res == -1:
                    continue
                if v == res:
                    colors[v] = 2
                    return res
                cycle.append(v)
                return res

    colors[v] = 2
    return -1

def find_cycle(vertices, edges):
    colors = [0 for _ in range(len(vertices))]
    cycle = []

    for v in vertices:
        if colors[v] == 0:
            compress_cycles_dfs(v, vertices, edges, colors, cycle)
            if cycle:
                return True, cycle

    return False, cycle

def compress_cycles(vertices, edges):
    cycle_exists, cycle = find_cycle(vertices, edges)

    if not cycle_exists:
        return vertices

    new_vertices = []
    new_edges = {}

    common_vertex = -1
    for v in vertices:
        if common_vertex == -1 and v in cycle:
            common_vertex = v

        new_v = common_vertex if v in cycle else v
        new_vertices.append(new_v)

        if v in edges.keys():
            for u in edges[v]:
                if common_vertex == -1 and u in cycle:
                    common_vertex = u
                new_u = common_vertex if u in cycle else u
                if new_v == new_u:
                    continue
                if not new_v in new_edges.keys():
                    new_edges.setdefault(new_v, set())
                new_edges[new_v].add(new_u)

    return compress_cycles(new_vertices, new_edges)

def find_path_dfs(parent, v, vertices, edges, colors, stack):
    colors[v] = 1

    if v in edges.keys():
        for u in edges[v]:
            if colors[u] == 0:
                find_path_dfs(v, u, vertices, edges, colors, stack)
            else:
                assert colors[u] == 2
                stack.append((v, u))

    if parent != -1:
        stack.append((parent, v))

    colors[v] = 2

def find_path(vertices, edges):
    colors = [0 for _ in range(len(vertices))]
    stack = []

    for v in vertices:
        if colors[v] == 0:
            find_path_dfs(-1, v, vertices, edges, colors, stack)

    return stack
