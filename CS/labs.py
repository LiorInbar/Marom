import marom
import re

page = marom.page()

page.set_url("http://www.cs.technion.ac.il/research-labs/")
#/li/a/text()
page.set_object_type_resource()
page.set_subject_query('//h1[text()="Research Labs"]/following-sibling::ul[position()=1]/li/a/text()')
def subject_func_lab(s):
	s = s.split()
	s = s[len(s)-1]
	s =  re.sub('[()]', '', s)
	return 'http://www.cs.technion.ac.il/research-labs/'+s
sf_lab = subject_func_lab
page.set_subject_func(sf_lab)
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Group')

page.set_object_type_string()
page.set_predicate('http://xmlns.com/foaf/0.1/name')
def object_func_name(s):
	return re.sub('[\n]',' ', s)
of_name = object_func_name
page.set_object_query('/text()')
page.set_object_func(of_name)
page.create_triples()

page.set_predicate('http://xmlns.com/foaf/0.1/homepage')
def object_func_homepage(s):
	return re.sub('[\n]','', s)
of_homepage = object_func_homepage
page.set_object_query('/@href')
page.set_object_func(of_homepage)
page.create_triples()

page.turtle("labs_turtle.txt")


