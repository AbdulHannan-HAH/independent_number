import networkx as nx
from itertools import combinations
import numpy as np

def numerical_semigroup_graph(generators):
    S = set()
    frontier = [0]
    max_limit = 200

    while frontier:
        current = frontier.pop(0)
        if current > max_limit:
            continue
        if current not in S:
            S.add(current)
            for g in generators:
                frontier.append(current + g)

    gaps = sorted([x for x in range(max(S)) if x not in S])

    if len(gaps) >= 2:
        max_check = gaps[-1] + gaps[-2]
    else:
        max_check = max(generators) * 3

    S.clear()
    frontier = [0]
    while frontier:
        current = frontier.pop(0)
        if current > max_check:
            continue
        if current not in S:
            S.add(current)
            for g in generators:
                frontier.append(current + g)

    gaps = sorted([x for x in range(max_check) if x not in S])

    G = nx.Graph()
    for gap in gaps:
        G.add_node(gap)

    edge_list = []
    for i, j in combinations(gaps, 2):
        if (i + j) in S:
            G.add_edge(i, j)
            edge_list.append((i, j, i + j))

    return G, gaps, edge_list

def perfect_circle_layout(G, gaps):
    pos = {}
    num_nodes = len(gaps)
    radius = 1.0

    for i, node in enumerate(sorted(gaps)):
        angle = 2 * np.pi * i / num_nodes - np.pi / 2
        pos[node] = (radius * np.cos(angle), radius * np.sin(angle))

    return pos

def find_maximum_independent_set(G):
    from networkx.algorithms.approximation import maximum_independent_set
    max_indep = maximum_independent_set(G)
    return max_indep, len(max_indep)

