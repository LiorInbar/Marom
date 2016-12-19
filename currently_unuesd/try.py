from rdflib import Graph
import pprint

g = Graph()
g.parse("triples.txt", format="nt")
print(len(g))
for stmt in g:
    pprint.pprint(stmt)