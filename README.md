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
  
  `import marom`  
    
  `p = page()`.  
  
  ## page methods:  
  
 the methods of a page object create triples using parameters loaded into them with setters methods.  
 
 create_triples():  
 the main method of the module - matching subjects to objects, both are achieved through xpath queries,
 via specific predicate. to use the methods, you have to load the following parameters to the  __page__ object 
 using the following setters:  
 set_url(url): the url of the webpage from which you extract the data  
 set_subject_query(query): xpath query for extracting the list of subjects
 set_subject_func(func): a function for proccesing the output of each element of the subject query output, or 0 if no 
 proccesing is needed.
 



  
we will present using of the module by extracting data and create triples from the staff page of the CS department - 
http://www.cs.technion.ac.il/people/faculty/.

