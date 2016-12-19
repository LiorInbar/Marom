from rdflib import Graph
import string

g = Graph()
prefix_map = {}
input_file = open('input_file_meta_triples.txt')
temp_file = open('temp_file_meta_triples.txt','r+')
lines=input_file.readlines()

for l in lines:
	h = l.split()
	if len(h)>0:
		if h[0]=='@prefix':
			t=len(h[2])-1
			prefix_map[h[1]]=h[2][1:t]

for l in lines:
	h = l.split()
	if len(h)>0:
		if h[0]!='@prefix':
			for w in h:
				for p in prefix_map.keys():
					w = w.replace(p,prefix_map[p])
				temp_file.write('<'+w+'>'+' ')
			temp_file.write(' .\n')


input_file.close()
temp_file.close()

g.parse("temp_file_meta_triples.txt", format="nt")
g.serialize(destination='turtle2.txt',format='turtle')
