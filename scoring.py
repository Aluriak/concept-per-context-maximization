"""Count the number of concept in a context"""

import clyngor


all_edges = set()

def accumulate(obj, att):
    all_edges.add('rel({},{})'.format(obj.number, att.number))
    return 'ok'

def reset():
    global all_edges
    all_edges = set()

def score():
    print(all_edges)
    ret = concept_number('.'.join(all_edges) + '.')
    reset()
    return ret


def concept_number(context:str):
    return sum(1 for model in clyngor.solve('enumerate_concepts.lp', inline=context))


def test_concept_number():
    assert concept_number('rel(1,2).') == 1
    assert concept_number('rel(a,b).') == 1
    assert concept_number('rel(a,b).rel(a,c).rel(d,c).') == 2
