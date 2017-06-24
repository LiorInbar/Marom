# marom
MAROM - Rdf Ontology Mapper

## installations:
the module works on python 2.  
external modules required:  
* lxml: processing xml documents and perform xpath queries - http://lxml.de/  
* rdflib: create turtle files - https://rdflib.readthedocs.io/en/stable/  
the marom module can be download from the project github page - download the file marom.py.   

## using the module: 
the module define the class __page__, which consists of a list of triples and the methods that create them.
to create and use __page__ instance, define page object with the constructor **page()**:  
  ```   
  import marom     
  page = page().  
  ```  
  
  ## page methods:  
  
 the methods of a page object create triples using parameters loaded into them with setters methods.  
 
 __create_triples()__:  
 the main method of the module - matching subjects to objects, both are achieved through xpath queries,
 via specific predicate. to use the methods, you have to load the following parameters to the  __page__ object 
 using the following setters:  
 __set_url(url)__: the url of the webpage from which you extract the data.  
 __set_subject_query__(query): xpath query for extracting the list of subjects.  
 __set_subject_func(func)__: a function for proccesing the output of each element of the subject query output, or 0 if no 
 proccesing is needed.  
 __set_predicate(predicate)__: the predicate of the triples.  
 __set_object_query(query)__: xpath query for extracting the list of objects.the query should be relative to the target
 element of the subject query. that is, the target element of the subject query is the root element of the object query.    
 __set_object_func(func)__: a function for proccesing the output of each element of the object query output, or 0 if no   
 proccesing is needed.    
 in adition, you will need to mention wethter the object of the triple is another RDF resource or a reguler string,  
 by either activate __set_object_type_resource()__ or __set_object_type_string()__.    
 after this settings, you can activate __create triples()__.  
 example:  
 we want to get student names from the page http://www.cs.technion.ac.il/people/graduate-students/. on the  "peoplelist" section we have:
   
   
**\<ul class="peoplelist">
 \<li>\<span class="nohomelink">\</span>\<a href="/people/sdolevfe/" title="Department info page for Dolev Adas">Adas, Dolev\</a>\</li>  
  \<li>\<span class="nohomelink">\</span>\<a href="/people/a.mohammad" title="Department info page for Mohammad   Agbarya">Agbarya,Mohammad\</a>\</li>** 
    
    
      
    for every student, we want the __href__ atribute of the __a__ element to be subject, with the prefix __'http://www.cs.technion.ac.il'__. the predicate is foaf:name. the name is the text of the __a__ element.
    the subect function add the __'http://www.cs.technion.ac.il'__ prefix, and we don't need object function.
    the object is not an RDF resource. then the code will be:  
   
  
```  
page.set_url("http://www.cs.technion.ac.il/people/graduate-students/")        
page.set_subject_query('//ul[@class="peoplelist"]/li/a[last()]/@href)
def subject_func_person(s):      
	return 'http://www.cs.technion.ac.il'+s    
sf_person = subject_func_person  
page.set_subject_func(sf_person)        
page.set_predicate('http://xmlns.com/foaf/0.1/name')    
page.set_object_query('/text()')    
page.set_object_func(0)    
page.set_object_type_string()    
page.create_triples() 
```  
   
the create_triple() method can generaly be used in almost every kind of triples extraction, but sometimes it is more comfortable to use 
some shortcuts. for example, sometimes we want our subject or object to be a some constant string, rather then the result of expath query. in this case, we can use the __add_triple_subject_xpath(object)__ or the __add_triple_object_xpath(subject)__ methods:  
in __add_triple_subject_xpath__, the object is a constant string, so you don't need to set the object query and function. instead you pass the object string as a parameter. similarly, in __add_triple_object_xpath(subject)__ the object is a constant string, so you don't need to set the subject query and function (the object query is relative to the root element).  
example:  
from the same page, we want to declare every student as an RDF resource of type foaf:Person. therefore we will create triples in which the object is the constant string 'http://xmlns.com/foaf/0.1/Person':  
  
  ```  
page.set_url("http://www.cs.technion.ac.il/people/graduate-students/")        
page.set_subject_query('//ul[@class="peoplelist"]/li/a[last()]/@href)
def subject_func_person(s):      
	return 'http://www.cs.technion.ac.il'+s    
sf_person = subject_func_person  
page.set_subject_func(sf_person)        
page.set_predicate('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')      
page.set_object_type_resource()    
page.add_triple_subject_xpath('http://xmlns.com/foaf/0.1/Person')
 
```  
  
  another option is simply add a single triple to the triples colection, with the function  
  __add_triple(subject,predicate,object)__ .  
  
  ## the triples colection  
    
 the triples colection is a list of map objects with fields 'subject', 'predicate, and 'object'.
 althogh it is better not to update this list directly (without using one of the above methods), it is posible, and sometimes neccesery.
  
 ##create the output file  
   
 After you finish to create triples, you turn the triples colection into RDF document with the method __turtle(file_name)__,
 flle_name is the name of the output file.
 
 
 
