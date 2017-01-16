import triples_creator
import re

url="http://www.cs.technion.ac.il/people/staff/"

subject_query_person='//table/tr/td[1]/a/@href'
def subject_func_person(s):
	return '<http://www.cs.technion.ac.il'+s+'>'
type_predicate = '<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
def object_func_person():
	return '<http://xmlns.com/foaf/0.1/Person>'
sf_person = subject_func_person
of_person = object_func_person

name_predicate = '<http://xmlns.com/foaf/0.1/name>'
name_query='/text()'
def object_func_name(s):
	return '"'+s+'"'
of_name = object_func_name

mbox_predicate = '<http://xmlns.com/foaf/0.1/mbox>'
mbox_query='/../../td[5]/text()'
def object_func_mbox(s):
	return s
of_mbox = object_func_mbox
'''base_query_group_1='//h1'
base_query_group_2='//h2'
subject_query_group='/text()'
object_query_group1='/..[position()=1]'
object_query_group2='/..[.>>//h2[1]]/h2[position() < .[position()]/last()/text()'''

group_query = '//table/caption/text()'
group_predicate = '<http://xmlns.com/foaf/0.1/Group>'
def subject_func_group(s):
	s = re.sub(' ','_',s)
	return '<http://www.cs.technion.ac.il/staff/'+s+'>'
def object_func_group():
	return '<http://xmlns.com/foaf/0.1/Group>'
sf_group = subject_func_group
of_group = object_func_group

member_predicate = '<http://xmlns.com/foaf/0.1/member>'
member_query = '/../tr/td/a[1]/@href'
def object_func_member(s):
	return '<http://www.cs.technion.ac.il'+s+'>'
of_member = object_func_member






triples = triples_creator.create_triples(url,subject_query_person,sf_person,type_predicate,0,of_person)
triples = triples + triples_creator.create_triples(url,subject_query_person,sf_person,name_predicate,name_query,of_name)
temp = triples_creator.create_triples(url,subject_query_person,sf_person,mbox_predicate,mbox_query,of_mbox)
for t in range(len(temp)):
	if t>0 :
		if temp[t]['subject']==temp[t-1]['subject']:
			triples.append({'subject' : temp[t]['subject'],'predicate' : mbox_predicate,'object' : '"'+temp[t-1]['object']+'@'+temp[t]['object']+'"'})
triples = triples + triples_creator.create_triples(url,group_query,sf_group,type_predicate,0,of_group)
triples = triples + triples_creator.create_triples(url,group_query,sf_group,member_predicate,member_query,of_member)


triples_creator.turtle(triples, 'staff_turtle.txt')

