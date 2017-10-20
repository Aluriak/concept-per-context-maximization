
main:
	python main.py


run:
	clingo run.lp -n 0

plot:
	python3 ~/scripts/plot/3D/cli.py solutions/upto4×4_stats.csv obj att "#concept"


t: tests
tests:
	python -m pytest *.py



neighbors:
	python clique_neighbors.py
size:
	python clique_size.py
