
import marom
import re

page = marom.page()

page.set_url("http://www.cs.technion.ac.il/people/faculty/")

page.set_object_type_resource()
def subject_func_person(s):
	return 'http://www.cs.technion.ac.il'+s
sf_person = subject_func_person
page.set_subject_query('//ul[@class="peoplelist"]/li/a[last()]/@href')
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
page.set_subject_func(sf_person)
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Person')


URIs = []
for a in page.triples:
	uri = a['subject']
	uri = re.sub(r'[<>]',"",uri)
	uri = re.sub(r'faculty/','',uri)
	URIs.append(uri)


page.set_predicate('http://xmlns.com/foaf/0.1/name')
page.set_subject_query('//ul[@class="peoplelist"]/li/a[last()]/@href')
page.set_object_query('/text()')
page.set_object_func(0)
page.set_object_type_string()
page.create_triples()


page.set_predicate('http://xmlns.com/foaf/0.1/homepage')
page.set_object_query('/../a/span[text()="[homepage]"]/../@href')
page.create_triples()


page.set_object_type_resource()
page.set_subject_query('//h2/text()')
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
def subject_func_group(s):
	s = re.sub(' ','_',s)
	return 'http://www.cs.technion.ac.il/faculty/'+s
sf_group = subject_func_group
page.set_subject_func(sf_group)
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Group')
page.add_triple('http://www.cs.technion.ac.il/faculty/Faculty','http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
		'http://xmlns.com/foaf/0.1/Group')



page.set_predicate('http://xmlns.com/foaf/0.1/member')
page.set_object_query('/following-sibling::ul[position()=1]/li/a[last()]/@href')
def object_func_member(s):
	return 'http://www.cs.technion.ac.il'+s
of_member = object_func_member
page.set_object_func(of_member)
page.create_triples()
page.add_triple_object_xpath('http://www.cs.technion.ac.il/faculty/Faculty')



def func_image(s):
	return 'http://www.cs.technion.ac.il'+s
f_image = func_image

temp = []
for uri in URIs:
	page.set_url(uri)
	page.set_subject_func(f_image)
	page.set_subject_query('//img[@class="personphoto"]/@src')
	page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
	page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Image')

	page.set_object_query('//img[@class="personphoto"]/@src')
	page.set_predicate('http://xmlns.com/foaf/0.1/image')
	page.set_object_func(f_image)
	page.add_triple_object_xpath(uri)

	
	page.set_object_query('//dt[text()="Email:"]/following-sibling::dd[position()=1]/text()')
	page.set_predicate('http://xmlns.com/foaf/0.1/mbox')
	page.set_object_type_string()
	page.set_object_func(0)
	page.add_triple_object_xpath(uri)
	if page.triples[len(page.triples)-1]['predicate']==page.triples[len(page.triples)-2]['predicate']:
		page.triples[len(page.triples)-2]['object']='"'+re.sub('"','',page.triples[len(page.triples)-2]['object'])+'@'+re.sub('"','',page.triples[len(page.triples)-1]['object'])+'"'
		del page.triples[len(page.triples)-1]
	
	page.set_object_query('//dt[text()="Phone:"]/following-sibling::dd[position()=1]/text()')
	page.set_predicate('http://xmlns.com/foaf/0.1/phone')
	page.set_object_func(0)
	page.add_triple_object_xpath(uri)


	infolist = page.evaluate_xpath('//dt[text()="Research interests"]/following-sibling::dd[position()=1]/text()')
	if len(infolist)>0:
		infolist[0]=infolist[0].replace('\r\n',' ')
		infolist[0]=infolist[0].replace('\n',' ')
		infolist[0]=infolist[0].replace('\r',' ')		
		infolist[0]=infolist[0].replace('.','')
		infolist[0]=infolist[0].replace('"','')
		if ';' in infolist[0]:
			infostring = infolist[0].split(';')
		else:
			infostring = infolist[0].split(',')
		for info in infostring:
			page.add_triple(uri,'http://xmlns.com/foaf/0.1/interest',info)




page.turtle('faculty_turtle.txt')

