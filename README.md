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


  
we will present using of the module by extracting data and create triples from the staff page of the CS department - 
http://www.cs.technion.ac.il/people/faculty/.

