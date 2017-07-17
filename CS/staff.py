import marom
import re



page = marom.page()
page.set_url("http://www.cs.technion.ac.il/people/staff/")


page.set_object_type_resource()
page.set_subject_query('//table/tr/td[1]/a/@href')
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
def subject_func_person(s):
	return 'http://www.cs.technion.ac.il'+s
sf_person = subject_func_person
page.set_subject_func(sf_person)
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Person')

URIs = []
for a in page.triples:
	uri = a['subject']
	uri = re.sub(r'[<>]',"",uri)
	uri = re.sub(r'staff/','',uri)
	URIs.append(uri)

page.set_subject_query('//table/tr/td[1]/a/@href')
page.set_predicate('http://xmlns.com/foaf/0.1/name')
page.set_object_query('/text()')
page.set_object_func(0)
page.set_object_type_string()
page.create_triples()

def object_func_mbox(s):
	return re.sub('"','',s)
mbox = object_func_mbox

page.set_predicate('http://xmlns.com/foaf/0.1/mbox')
page.set_object_query('/../../td/img/../text()')
page.set_object_func(mbox)
page.create_triples()
t=0
while t < len(page.triples):
	if t>0:
		if page.triples[t]['predicate']=='http://xmlns.com/foaf/0.1/mbox' and page.triples[t]['subject']==page.triples[t-1]['subject']:
			page.triples[t]['object']=page.triples[t-1]['object']+'@'+page.triples[t]['object']
			del page.triples[t-1]
			t=t-1
	t=t+1

page.set_object_type_resource()
def subject_func_group(s):
	s = re.sub(' ','_',s)
	return 'http://www.cs.technion.ac.il/staff/'+s
sf_group = subject_func_group
page.set_subject_func(sf_group)
page.set_subject_query('//table/caption/text()')
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Group')


page.set_predicate('http://xmlns.com/foaf/0.1/member')
page.set_subject_query('//table/caption/text()')
page.set_object_query('/../tr/td/a[1]/@href')
def object_func_member(s):
	return 'http://www.cs.technion.ac.il'+s
of_member = object_func_member
page.set_object_func(of_member)
page.create_triples()


def subject_func_image(s):
	return 'http://www.cs.technion.ac.il'+s
sf_image = subject_func_image

for uri in URIs:
	page.set_url(uri)
	page.set_subject_query('//img[@class="personphoto"]/@src')
	page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
	page.set_subject_func(sf_image) 
	page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Image')

	page.set_object_query('//img[@class="personphoto"]/@src')
	page.set_predicate('http://xmlns.com/foaf/0.1/img')
	page.set_object_func(sf_image)
	page.add_triple_object_xpath(uri)

	page.set_object_type_string()
	page.set_object_query('//dt[text()="Phone:"]/following-sibling::dd[position()=1]/text()')
	page.set_predicate('http://xmlns.com/foaf/0.1/phone')
	page.set_object_func(0)
	page.add_triple_object_xpath(uri)

page.turtle('staff_turtle.txt')

