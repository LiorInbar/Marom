#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET
from rdflib import Graph
import string
import fileinput
import re


def encoding_fix(text):
	#return re.sub(b'\xc3\x97\xc2',b'\xd7',unicode(text).encode('utf-8')).decode('utf-8')
	return text



class page:

	def __init__(self):
		self.triples = []		
	def set_url(self, url):
		self.url = url
	def get_url(self):
		return self.url	
	def set_subject_query(self, query):
		self.subject_query = query
	def set_subject_func(self,func):
		self.subject_func = func
	def set_predicate(self,predicate):
		self.predicate = predicate
	def set_object_query(self,query):
		self.object_query = query
	def set_object_func(self,func):
		self.object_func = func
	def evaluate_xpath(self,query):
		data = urllib.request.urlopen(self.get_url()).read()
		tree = etree.HTML(data)
		result = tree.xpath(query)
		for i in range(len(result)):
			result[i]=encoding_fix(result[i])
		return result
	def add_triple(self,subject,predicate,Object):
		self.triples.append({})
		self.triples[len(self.triples)-1]['subject'] = '<'+subject+'>'
		self.triples[len(self.triples)-1]['predicate'] = '<'+predicate+'>'
		if(self.object_type=="resource"):
		    self.triples[len(self.triples)-1]['object'] = '<'+ Object+'>'
		if(self.object_type=="string"):
		    self.triples[len(self.triples)-1]['object'] = '"'+Object+'"'
	def set_object_type_resource(self):
		self.object_type = "resource"
	def set_object_type_string(self):
		self.object_type = "string"


	def create_triples(self):
	    page = urllib.request.urlopen(self.url).read()
	    tree = etree.HTML(page)
	    new_triples = []
	    if self.subject_query!=0:
	        isproperty = re.search(r'(/@[^/]*\Z)',self.subject_query)
	        istext = re.search(r'text\(\)\Z',self.subject_query)
	        modified_query = re.sub(r'/@[^/]*\Z','',self.subject_query) 
	        modified_query = re.sub(r'/text\(\)\Z','',modified_query)
	        subejct_elements = tree.xpath(modified_query)
	        for element in subejct_elements:
	            path = etree.ElementTree(tree).getpath(element)
	            if istext:
	                subject = self.subject_func(tree.xpath(path+'/text()')[0]) if self.subject_func!=0 else tree.xpath(path+'/text()')[0]
	            elif isproperty:
	                subject = self.subject_func(tree.xpath(path+isproperty.group())[0]) if self.subject_func!=0 else tree.xpath(path+isproperty.group())[0]
	            else:
	                subject = self.subject_func(element) if self.subject_func!=0 else element
	            if len(subject) == 0:
	                continue                        
	            if  self.object_query != 0:   
	                Object_result = tree.xpath(path+self.object_query)
	                if len(Object_result) == 0:
	                    continue
	            else:
	                Object_result = [self.object_func()]
	            for Object in Object_result:
	                if self.object_query != 0:
	                    if self.object_func!=0:
	                   	    Object = self.object_func(Object)
	                new_triples.append({})
	                new_triples[len(new_triples)-1]['subject'] = '<'+encoding_fix(subject)+'>'
	                new_triples[len(new_triples)-1]['predicate'] = '<'+self.predicate+'>'
	                if(self.object_type=="resource"):
	                    new_triples[len(new_triples)-1]['object'] = '<'+encoding_fix(Object)+'>'
	                if(self.object_type=="string"):
	                    new_triples[len(new_triples)-1]['object'] = '"'+encoding_fix(Object)+'"'
	    self.triples = self.triples + new_triples

	def add_triple_object_xpath(self,subject):
	    page = urllib.request.urlopen(self.get_url()).read()
	    tree = etree.HTML(page)
	    result = tree.xpath(self.object_query)
	    for i in range(len(result)):
		    self.triples.append({})
		    self.triples[len(self.triples)-1]['subject'] = '<'+subject+'>'
		    self.triples[len(self.triples)-1]['predicate'] = '<'+self.predicate+'>'
		    if self.object_func!=0:
		        if(self.object_type=="resource"):
		            self.triples[len(self.triples)-1]['object'] = '<'+ self.object_func(encoding_fix(result[i]))+'>'
		        if(self.object_type=="string"):
		            self.triples[len(self.triples)-1]['object'] = '"'+self.object_func(encoding_fix(result[i]))+'"'
		    else:
		        if(self.object_type=="resource"):
		            self.triples[len(self.triples)-1]['object'] = '<'+ encoding_fix(result[i])+'>'
		        if(self.object_type=="string"):
		            self.triples[len(self.triples)-1]['object'] = '"'+encoding_fix(result[i])+'"'		    	


	def add_triple_subject_xpath(self,Object):
	    page = urllib.request.urlopen(self.get_url()).read()
	    tree = etree.HTML(page)
	    result = tree.xpath(self.subject_query)
	    for i in range(len(result)):
		    self.triples.append({})
		    self.triples[len(self.triples)-1]['subject'] = '<'+self.subject_func(encoding_fix(result[i]))+'>' if self.subject_func!=0 else '<'+encoding_fix(result[i])+'>'	    
		    self.triples[len(self.triples)-1]['predicate'] = '<'+self.predicate+'>'
		    if(self.object_type=="resource"):
		        self.triples[len(self.triples)-1]['object'] = '<'+ Object+'>'
		    if(self.object_type=="string"):
		        self.triples[len(self.triples)-1]['object'] = '"'+Object+'"'

	def turtle(self,output_file):
	    nt = open(output_file,'w')
	    for triples_iterator in range(len(self.triples)):
	        nt.write(self.triples[triples_iterator]['subject']+' '+
	            self.triples[triples_iterator]['predicate']+' '+
	            self.triples[triples_iterator]['object']+' '+'.\n')
	    nt.close()
	    g = Graph()
	    g.parse(output_file, format="nt")
	    g.serialize(destination=output_file,format='turtle')
	    for line in fileinput.input(output_file, inplace=True):
	        print(line.replace('ns1:','foaf:').rstrip())   



