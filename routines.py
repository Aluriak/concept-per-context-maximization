"""Various routines.

"""
import itertools
from collections import defaultdict
import clyngor


def number_of_concepts_in(context:str):
    """Return the number of concepts found in given context built by rel/2 atoms"""
    models = clyngor.solve('enumerate_concepts.lp', inline=context)
    return sum(1 for _ in models)

def build_clique(nodes:tuple) -> str:
    """Return string containing rel/2 atoms building a cliques with given nodes"""
    def gen():
        for s, t in itertools.permutations(nodes, 2):
            yield 'rel({},{}).'.format(s,t)
    return ''.join(gen())


def draw_context(atoms:iter):
    """Draw given context is stdout"""
    # print('JJONNY:', type(atoms))
    # print('AMONDS:', atoms)
    if isinstance(atoms, str):
        atoms = next(clyngor.solve([], inline=atoms).int_not_parsed)
    # print('JJONNY:', type(atoms))
    # print('AMONDS:', tuple(atoms))
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
