
import triples_creator

url="http://www.cs.technion.ac.il/people/faculty/"
subject_query_person='//ul[@class="peoplelist"]/li/a[last()]/@href'
def subject_func_person(s):
	return '<http://www.cs.technion.ac.il'+s+'>'
type_predicate = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
def object_func_person():
	return '<http://xmlns.com/foaf/0.1/Person>'
sf_person = subject_func_person
of_person = object_func_person

triples = triples_creator.create_triples(url,subject_query_person,sf_person,type_predicate,0,of_person)

name_predicate = '<http://xmlns.com/foaf/0.1/name>'
name_query='/text()'
def object_func_name(s):
	return '"'+s+'"'
of_name = object_func_name

triples = triples + triples_creator.create_triples(url,subject_query_person,
	sf_person,name_predicate,name_query,of_name)


homepage_predicate = '<http://xmlns.com/foaf/0.1/homepage>'
homepage_query='/../a[1]/@href'
def object_func_homepage(s):
	return '"'+s+'"'
of_homepage = object_func_homepage
triples = triples + triples_creator.create_triples(url,subject_query_person,
	sf_person,homepage_predicate,homepage_query,of_homepage)	


triples_creator.turtle(triples, 'faculty_example_turtle.txt')

