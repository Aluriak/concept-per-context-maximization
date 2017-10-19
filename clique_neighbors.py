"""Study of the behavior of clique neighborood.

"""

import csv
import clyngor
import itertools
from collections import defaultdict
from main import draw_context


CLIQUE_SIZE = 4
MAX_NEIGHBOR = 2


def build_clique(nodes:tuple) -> str:
    """Return string containing ASP code"""
    def gen():
        for s, t in itertools.permutations(nodes, 2):
            yield 'rel({},{}).'.format(s,t)
    return ''.join(gen())


def supplementary_relations(nodes:tuple, max_neighbors:int) -> str:
    """Yield strings containing ASP code describing a possible neighborood
    for a clique of given size.
    """
    def all_combinations(tps:tuple, start:int=1) -> iter:
        for size in range(start, 1+len(tps)):
            yield from itertools.combinations(tps, size)

    neighbors = tuple(range(len(nodes) + 1, len(nodes) + 1 + max_neighbors))
    assert set(neighbors) & set(nodes) == set()
    possible_neighbors = nodes + neighbors
    # possible_neighbors = nodes  # neighbors can't form cliques
    combi_per_neighbor = tuple(all_combinations(possible_neighbors) for _ in range(max_neighbors))
    for neighbors in itertools.product(*combi_per_neighbor):
        # print('JJONNY:', neighbors)
        # print('VCFCOB:', tuple(enumerate(neighbors, start=1+len(nodes))))
        yield ''.join('rel({a},{b}).rel({b},{a}).'.format(a=neighbor, b=node) if node else ''
                      for neighbor, nodes in enumerate(neighbors, start=1+len(nodes))
                      for node in nodes)



def try_adding_concepts_by_adding_relations():
    nodes = tuple(range(1, CLIQUE_SIZE+1))
    clique = build_clique(nodes)
    clique_score = sum(1 for _ in clyngor.solve('enumerate_concepts.lp', inline=clique))
    best_atoms, best_score = [], 0
    best_neighbors, best_addition = [], 0
    for idx, added_objs in enumerate(supplementary_relations(nodes, MAX_NEIGHBOR)):
        print('\rCONTEXTS: {}\t\tBEST SOLUTION: {}'.format(idx, best_score), end='', flush=True)
        context = added_objs + clique
        nb_added_relations = added_objs.count('.')
        models = clyngor.solve('enumerate_concepts.lp', inline=context)
        nb_concept = sum(1 for _ in models)
        # Register the best score, i.e. the sets of neighbors that maximize
        #  the number of concepts in the context.
        if nb_concept > best_score:
            best_score = nb_concept
            best_atoms = [context]
        elif nb_concept == best_score:
            best_atoms.append(context)
        # Register the best neighborood, i.e. the greater set of neighbors
        #  that keeps the number of concepts low.
        if nb_concept == clique_score:
            if nb_added_relations > best_addition:
                best_addition = nb_added_relations
                best_neighbors = [context]
            elif nb_added_relations == best_addition:
                best_neighbors.append(context)

    print()
    print('#' * 80, '\nGREATER SCORES')
    print('Maximal number of concepts')
    for atoms in best_atoms:
        draw_context(atoms)
        print()
    print('BEST SOLUTIONS:')
    print('CONCEPTS:', best_score, '({} in clique alone)'.format(clique_score))
    print('NUMBER OF SOLUTIONS:', len(best_atoms))
    print()
    print('#' * 80, '\nGREATER NEIGHBORS')
    print('Maximal number of neighbors that do not raise the number of concepts')
    for atoms in best_neighbors:
        draw_context(atoms)
        print()
    print('BEST SOLUTIONS:')
    print('NUMBER OF NEIGHBORS:', best_addition)
    print('NUMBER OF SOLUTIONS:', len(best_neighbors))
    return best_score


if __name__ == "__main__":
    try_adding_concepts_by_adding_relations()
