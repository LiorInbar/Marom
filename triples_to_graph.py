import triples_creator

url="http://www.cs.technion.ac.il/people/faculty/index.html"
querry1='//ul[@class="peoplelist"]/li/a[2]/@href'
querry2='/./../text()'
querry3='/./../../a[1]/@href'
output =  open('graph.txt', 'w')
format1 = '<http://www.cs.technion.ac.il@> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .'
format2 ='<http://www.cs.technion.ac.il@> <http://xmlns.com/foaf/0.1/name> "@@"" .'  
format3 = '<http://www.cs.technion.ac.il@>  <http://xmlns.com/foaf/0.1/homepage>  "@@"" .'

triples_creator.create_triples(url,format1,output,querry1)
triples_creator.create_triples(url,format2,output,querry1,querry2)
triples_creator.create_triples(url,format3,output,querry1,querry3)

output.close()

from rdflib import Graph
import string
g = Graph()
g.parse("graph.txt", format="nt")
g.serialize(destination='turtle.txt',format='turtle')

input_file=open('turtle.txt')
final_output=open('final_output.txt','w')
lines=input_file.readlines()
for l in lines:
	l=string.replace(l,'ns1:','foaf:')
	final_output.write(l);






