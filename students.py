import triples_creator
import re

url="http://www.cs.technion.ac.il/people/graduate-students/"

subject_query_person='//ul[@class="peoplelist"]/li/a[last()]/@href'
def subject_func_person(s):
	return '<http://www.cs.technion.ac.il'+s+'>'
type_predicate = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
def object_func_person():
	return '<http://xmlns.com/foaf/0.1/Person>'
sf_person = subject_func_person
of_person = object_func_person

homepage_query='/../a[1]/@href'
homepage_predicate = '<http://xmlns.com/foaf/0.1/homepage>'
def object_func_homepage(s):
	return '"'+s+'"'

name_query='/text()'
name_predicate = '<http://xmlns.com/foaf/0.1/name>'
def object_func_name(s):
	return '"'+s+'"'

group_query = '//h2/text()'
group_predicate = '<http://xmlns.com/foaf/0.1/Group>'
def subject_func_group(s):
	s = re.sub(' ','_',s)
	return '<http://www.cs.technion.ac.il/students/'+s+'>'
def object_func_group():
	return '<http://xmlns.com/foaf/0.1/Group>'
sf_group = subject_func_group
of_group = object_func_group

member_predicate = '<http://xmlns.com/foaf/0.1/member>'
member_query = '/following-sibling::ul[position()=1]/li/a[last()]/@href'
def object_func_member(s):
	return '<http://www.cs.technion.ac.il'+s+'>'
of_member = object_func_member









def subject_func_group(s):
	s = re.sub(' ','_', s)
	return '<http://www.cs.technion.ac.il/faculty/'+s+'>'
def object_func_Group():
	return '<http://xmlns.com/foaf/0.1/Group>'
member_predicate = '<http://xmlns.com/foaf/0.1/member>'
	 

of_homepage = object_func_homepage
of_name = object_func_name
sf_group = subject_func_group
of_group = object_func_Group


triples = triples_creator.create_triples(url,subject_query_person,sf_person,type_predicate,0,of_person)
triples = triples + triples_creator.create_triples(url,subject_query_person,sf_person,homepage_predicate,homepage_query,of_homepage)	
triples = triples + triples_creator.create_triples(url,subject_query_person,sf_person,name_predicate,name_query,of_name)
triples = triples + triples_creator.create_triples(url,group_query,sf_group,type_predicate,0,of_group)
triples = triples + triples_creator.create_triples(url,group_query,sf_group,member_predicate,member_query,of_member)

triples_creator.turtle(triples, 'students_turtle.txt')

