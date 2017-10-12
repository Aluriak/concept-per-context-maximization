
import csv
import clyngor
import itertools
from collections import defaultdict


MAX_DIM_SIZE = 3
# MAX_DIM_SIZE = 4  # much more longer


def draw_context(atoms:iter):
    """Draw given context is stdout"""
    objs, atts = set(), set()
    have = defaultdict(set)
    for _, (obj, att) in atoms:
        objs.add(obj)
        atts.add(att)
        have[obj].add(att)
    objs = sorted(objs)
    atts = sorted(atts)
    obj_max_width = max(len(obj) for obj in objs)
    att_max_width = max(len(att) for att in atts)
    print(' ' * obj_max_width, '|', ' | '.join(att.center(att_max_width) for att in atts))
    for obj in objs:
        print(obj.rjust(obj_max_width), '|', ' | '.join(('X' if att in have[obj] else ' ').center(att_max_width) for att in atts))


def max_number_of_concepts(nobj:int, natt:int):
    best_atoms, best_score = [], 0
    contexts = clyngor.solve('enumerate_contexts.lp', constants={'nobj': nobj, 'natt': natt}).int_not_parsed
    for idx, atoms in enumerate(contexts):
        print('\rCONTEXTS: {}\t\tBEST SOLUTION: {}'.format(idx, best_score), end='', flush=True)
        nb_atoms = len(atoms)
        # print(atoms)
        patoms = clyngor.utils.answer_set_to_str(atoms, '.') + '.'
        # print(patoms)
        nb_concept = sum(1 for _ in clyngor.solve('enumerate_concepts.lp', inline=patoms))
        if nb_concept > best_score:
            best_score = nb_concept
            best_atoms = [atoms]
        elif nb_concept == best_score:
            best_atoms.append(atoms)
    print()

    print('BEST SOLUTIONS:')
    print('CONCEPTS:', best_score)
    for atoms in best_atoms:
        print()
        draw_context(atoms)
    return best_score


if __name__ == "__main__":
    outfile = 'solutions/full_stats.csv'
    with open(outfile, 'w') as fd:
        writer = csv.writer(fd, delimiter=',')
        writer.writerow(['obj', 'att', '#concept'])
        for nobj, natt in itertools.product(range(1, MAX_DIM_SIZE + 1), repeat=2):
            nbc = max_number_of_concepts(nobj, natt)
            writer.writerow([nobj, natt, nbc])
    print('Finished ! Data written into `{}`.'.format(outfile))
