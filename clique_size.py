"""Computation of the number of concept for a clique of size n"""


from routines import build_clique, build_biclique, number_of_concepts_in, concepts_in, pretty_concept

MINSIZE, MAXSIZE = 1, 10

def get_clique_table(min_size:int, max_size:int):
    sizes, concepts = [], []
    for size in range(1, max_size+1):
        clique = build_clique(range(size))
        sizes.append(str(size).rjust(5))
        concepts.append(str(number_of_concepts_in(clique)).rjust(5))

    template = r"""
\begin{{table}}[H]
    \centering\begin{{tabular}}{{|l|{}|}}
        \hline
         clique size  & {} \\\hline
         \#concepts   & {} \\\hline
    \end{{tabular}}
    \caption{{Number of concepts produced by a clique of given size in a non-reflexive graph context. In a reflexive graph context, one concept covers each maximal clique independently of it size.}}
    \label{{tab:pgfca:clique-as-concepts}}
\end{{table}}
    """

    print(template.strip().format('|'.join('c' for _ in sizes), ' & '.join(sizes), ' & '.join(concepts)))


def get_biclique_table(min_size:int, max_size:int):
    sizes, concepts = [], []
    for size in range(1, max_size+1):
        biclique = build_biclique(range(size), range(size, size*2), add_reflexive_edges=True)
        sizes.append(str(size).rjust(5))
        concepts.append(str(number_of_concepts_in(biclique)).rjust(5))
        if size == 2:
            for ext, int in concepts_in(biclique):
                print(pretty_concept(ext, int))

    template = r"""
\begin{{table}}[H]
    \centering\begin{{tabular}}{{|l|{}|}}
        \hline
        biclique size & {} \\\hline
         \#concepts   & {} \\\hline
    \end{{tabular}}
    \caption{{Number of concepts produced by a biclique of given size in a reflexive graph context. Biclique size refers to the number of nodes in \textit{{each}} set. In a non-reflexive graph context, one concept covers each maximal biclique independently of it size.}}
    \label{{tab:pgfca:biclique-as-concepts}}
\end{{table}}
    """

    print(template.strip().format('|'.join('c' for _ in sizes), ' & '.join(sizes), ' & '.join(concepts)))


if __name__ == "__main__":
    get_clique_table(MINSIZE, MAXSIZE)
    get_biclique_table(MINSIZE, MAXSIZE)
