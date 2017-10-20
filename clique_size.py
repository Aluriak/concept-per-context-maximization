"""Computation of the number of concept for a clique of size n"""


from routines import build_clique, number_of_concepts_in


def run(max_size:int=15):
    sizes, concepts = [], []
    for size in range(3, max_size+1):
        clique = build_clique(range(size))
        sizes.append(size)
        concepts.append(number_of_concepts_in(clique))

    print(r'\begin{{tabular}}[|{}|]'.format('|'.join('c' for _ in sizes)))
    print('   ', ' & '.join(map(str, sizes)), r'\\')
    print('   ', ' & '.join(map(str, concepts)), r'\\')
    print(r'\end{tabular}')


if __name__ == "__main__":
    run()
