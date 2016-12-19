import triples_creator

url="http://www.cs.technion.ac.il/people/faculty/index.html"
querry1='//ul[@class="peoplelist"]/li/a[2]/@href'
querry2='/./../text()'
querry3='/./../../a[1]/@href'
output =  open('output_file.txt', 'w')
format1 = 'http://www.cs.technion.ac.il@ a foaf:Person'
format2 ='http://www.cs.technion.ac.il@ foaf:name @@'  
format3 = 'http://www.cs.technion.ac.il@  foaf:homepage  @@'

triples_creator.create_triples(url,format1,output,querry1)
triples_creator.create_triples(url,format2,output,querry1,querry2)
triples_creator.create_triples(url,format3,output,querry1,querry3)



output.close()