import triples_creator
import re

url="http://www.cs.technion.ac.il/research-labs/"
query1='//ul[2]/li'
query2='/a/text()'
query3='/a/@href'
output =  open('docs_output.txt', 'w')
format1 = 'http://www.cs.technion.ac.il/research-labs/@ a foaf:Group'
format2 ='http://www.cs.technion.ac.il/research-labs/@ foaf:name @@'  
format3 = 'http://www.cs.technion.ac.il/research-labs/@  foaf:homepage  @@'

def group_func(s):
	s = s.split()
	s = s[len(s)-1]
	return re.sub('[()]', '', s)

def name_func(s):
	return re.sub('[\n]',' ', s)

def hompage_func(s):
	return re.sub('[\n]','', s)
	 
func1 = group_func
func2 = name_func
func3 = hompage_func

triples_creator.create_triples_3(url,format1,output,query1,query2,func1,0,0)	
triples_creator.create_triples_3(url,format2,output,query1,query2,func1,query2,func2)
triples_creator.create_triples_3(url,format3,output,query1,query2,func1,query3,func3)



output.close()