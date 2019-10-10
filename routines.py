"""Various routines.

"""
import itertools
from collections import defaultdict
import clyngor


def concepts_in(context:str):
    """Return the concepts found in given context built by rel/2 atoms"""
    models = clyngor.solve('enumerate_concepts.lp', inline=context).by_predicate
    for model in models:
        extent = frozenset(args[0] for args in model.get('obj', ()) if len(args) == 1)
        intent = frozenset(args[0] for args in model.get('att', ()) if len(args) == 1)
        yield extent, intent

def number_of_concepts_in(context:str):
    """Return the number of concepts found in given context built by rel/2 atoms"""
    return sum(1 for _ in concepts_in(context))

def build_clique(nodes:tuple) -> str:
    """Return string containing rel/2 atoms building a cliques with given nodes"""
    def gen():
        for s, t in itertools.permutations(nodes, 2):
            yield 'rel({},{}).'.format(s,t)
    return ''.join(gen())

def build_biclique(seta:tuple, setb:tuple, add_reflexive_edges:bool=False) -> str:
    """Return string containing rel/2 atoms building a cliques with given nodes"""
    def gen():
        for s, t in itertools.product(seta, setb):
            yield 'rel({},{}).'.format(s,t)
        if add_reflexive_edges:
            for n in itertools.chain(seta, setb):
                yield 'rel({},{}).'.format(n,n)
    return ''.join(gen())

def pretty_concept(ext:set, int:set, *, sep=',') -> str:
    pretty = lambda s: '{' + sep.join(map(str, sorted(tuple(s)))) + '}'
    return pretty(ext) + ' × ' + pretty(int)

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
