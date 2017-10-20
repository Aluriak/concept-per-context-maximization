"""Study of the behavior of clique neighborood.

"""

import csv
import math
import clyngor
import itertools
from collections import defaultdict, Counter
from routines import draw_context, build_clique, number_of_concepts_in


CLIQUE_SIZE = 4
MAX_NEIGHBOR = 2


def supplementary_relations(nodes:tuple, max_neighbors:int, allow_linked_neighbors:bool=True) -> str:
    """Yield strings containing ASP code describing a possible neighborood
    for a clique of given size.

    nodes -- the nodes of the clique
    max_neighbors -- the maximal number of considered neighbors for each dimension
    allow_linked_neighbors -- if True, allow added nodes to be in relation to each others

    """
    def all_combinations(tps:tuple, start:int=1) -> iter:
        for size in range(start, 1+len(tps)):
            yield from itertools.combinations(tps, size)

    neighbors = tuple(range(len(nodes) + 1, len(nodes) + 1 + max_neighbors))
    assert set(neighbors) & set(nodes) == set()
    possible_neighbors = nodes + (neighbors if allow_linked_neighbors else ())
    combi_per_neighbor = tuple(all_combinations(possible_neighbors) for _ in range(max_neighbors))
    for neighbors in itertools.product(*combi_per_neighbor):
        # print('JJONNY:', neighbors)
        # print('VCFCOB:', tuple(enumerate(neighbors, start=1+len(nodes))))
        yield ''.join('rel({a},{b}).rel({b},{a}).'.format(a=neighbor, b=node) if node else ''
                      for neighbor, nodes in enumerate(neighbors, start=1+len(nodes))
                      for node in nodes)


def print_clique_neighborhood_study(allow_linked_neighbors:bool=True):
    nodes = tuple(range(1, CLIQUE_SIZE+1))
    clique = build_clique(nodes)
    clique_score = sum(1 for _ in clyngor.solve('enumerate_concepts.lp', inline=clique))

    # measures, each associated with the best score, and the set of contexts reaching it
    # max(#concept): which neighborhoods maximize the number of concepts
    maximize_concept_number_atoms, maximize_concept_number_score = [], 0
    # max(silent): which maximal neighborhoods keeps the same number of concepts
    maximize_silent_neighbor_atoms, maximize_silent_neighbor_score = [], 0
    # min(noisy): which minimal neighborhoods increase the number of concepts
    minimize_noisy_neighbor_atoms, minimize_noisy_neighbor_score = [], math.inf
    minimize_noisy_neighbor_nb_concept = []  # number of concepts

    for idx, added_objs in enumerate(supplementary_relations(nodes, MAX_NEIGHBOR, allow_linked_neighbors=allow_linked_neighbors)):
        print("\rCONTEXTS: {}\t\tGREATER #CONCEPT: {}\t\tMAX(SILENT): {}\t\tMIN(NOISY): {}                                  "
              "".format(idx, maximize_concept_number_score, maximize_concept_number_score, minimize_noisy_neighbor_score), end='', flush=True)
        context = added_objs + clique
        nb_added_relations = added_objs.count('.')
        nb_concept = number_of_concepts_in(context)

        # Register the best nb_concept maximizer, i.e.
        # the sets of neighbors that maximize the number of concepts in the context.
        if nb_concept > maximize_concept_number_score:
            maximize_concept_number_score = nb_concept
            maximize_concept_number_atoms = [context]
        elif nb_concept == maximize_concept_number_score:
            maximize_concept_number_atoms.append(context)

        # Register the silent neighborood, i.e. the greater set of neighbors
        #  that keeps the number of concepts equals to the clique alone.
        if nb_concept == clique_score:
            if nb_added_relations > maximize_silent_neighbor_score:
                maximize_silent_neighbor_score = nb_added_relations
                maximize_silent_neighbor_atoms = [context]
            elif nb_added_relations == maximize_silent_neighbor_score:
                maximize_silent_neighbor_atoms.append(context)

        # Register the smaller noisy neighborood, i.e. the smaller set of neighbors
        #  that increase the number of concepts.
        if nb_concept > clique_score:
            # if nb_added_relations <= minimize_noisy_neighbor_score: # common treatment
                # minimize_noisy_neighbor_nb_concept.append(nb_concept - clique_score)
            if nb_added_relations < minimize_noisy_neighbor_score:
                minimize_noisy_neighbor_score = nb_added_relations
                minimize_noisy_neighbor_atoms = [context]
                minimize_noisy_neighbor_nb_concept = [nb_concept - clique_score]
            elif nb_added_relations == minimize_noisy_neighbor_score:
                minimize_noisy_neighbor_atoms.append(context)
                minimize_noisy_neighbor_nb_concept.append(nb_concept - clique_score)

    # NOTE: the number of neighbors added is two times lower than the showed
    #  context, because the graph is undirected.
    print()
    print('#' * 80, '\nGREATER NEIGHBORS')
    print('Maximizing the number of concepts')
    for atoms in maximize_concept_number_atoms:
        draw_context(atoms)
        print()
    print('BEST SOLUTIONS:')
    print('CONCEPTS:', maximize_concept_number_score, '({} in clique alone)'.format(clique_score))
    print('NUMBER OF SOLUTIONS:', len(maximize_concept_number_atoms))

    print()
    print('#' * 80, '\nSILENT NEIGHBORS')
    print('Maximal number of neighbors that do not raise the number of concepts')
    for atoms in maximize_silent_neighbor_atoms:
        draw_context(atoms)
        print()
    print('BEST SOLUTIONS:')
    print('NUMBER OF NEIGHBORS:', maximize_silent_neighbor_score)
    print('NUMBER OF SOLUTIONS:', len(maximize_silent_neighbor_atoms))

    print()
    print('#' * 80, '\nNOISER NEIGHBORS')
    print('Minimal number of neighbors raising the number of concepts')
    for atoms in minimize_noisy_neighbor_atoms:
        draw_context(atoms)
        print()
    print('BEST SOLUTIONS:')
    print('NUMBER OF NEIGHBORS:', minimize_noisy_neighbor_score)
    print('NUMBER OF SOLUTIONS:', len(minimize_noisy_neighbor_atoms))
    print('NUMBER OF CONCEPTS ADDED:', ', '.join('{} concept {} times'.format(n, nb) for n, nb in sorted(Counter(minimize_noisy_neighbor_nb_concept).items(), key=lambda x:x[0])))


if __name__ == "__main__":
    print_clique_neighborhood_study(allow_linked_neighbors=True)
