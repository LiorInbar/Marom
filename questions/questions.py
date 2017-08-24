#!/usr/bin/env python
# -*- coding: utf-8 -*-

import marom

import urllib
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET
from rdflib import Graph
import string
import fileinput
import re
import sys

def annoying_hebrew_issues(s):
	temp=b'|\x20|\x21|\x22\x23|\x24|\x25|\x26|\x27|\x28|\x29|\x30|\x31|\x32|\x33|\x34|\x35|\x36|\x37|\x38|\x39|\x2c|\x2d|\x3a|\x3b|\x3c|\x3d|\x3e|'
	special=b'\xd7'
	weird=b'\xc3\x97\xc2'
	bad=b'\x10|\x11|\x12|\x13|\x14|\x15|\x16|\x17|\x18|\x19'
	bad2=b'\x40|\x41|\x42|\x43|\x44|\x45|\x46|\x47|\x48|\x49|\x50|\x51|\x52|\x53|\x54|\x55|\x56|\x57|\x58|\x59|\x60|\x61|\x62|\x63|\x64|\x65|\x66|\x67|\x68|\x69|\x70|\x71'
	bad3=b'\x72|\x73|\x74|\x75|\x76|\x77|\x78|\x79|\x80|\x81|\x82|\x83|\x84|\x85|\x86|\x87|\x88|\x89|\xb0|\xb1|\xb2|\xb3|\xb4|\xb5|\xb6|\xb7|\xb8|\xb9|\xc0|\xc1|\xc2|\xc3|\xc4|\xc5|\xc6|\xc7|\xc8|\xc9|\xd0|\xd1|\xd2|\xd3|\xd4|\xd5|\xd6|\xd8|\xd9|\xe0|\xe1|\xe2|\xe3'
	bad4=b'\xe4|\xe5|\xe6|\xe7|\xe8|\xe9|\x1a|\x1b|\x1c|\x1d|\x1e'
	bad5=b'\x4a|\x4b|\x4c|\x4d|\x4e|\x5a|\x5b|\x5c|\x5d|\x5e|\x6a|\xab|\xac|\xad|\xae|\xba|\xbb|\xbc|\xbd|\xbe|\xca|\xcb|\xcc|\xcd|\xce|\xda|\xdb|\xdc|\xdd|\xde|\xea|\xeb|\xec|\xed|\xee|\x6b|\x6c|\x6d|\x6e|\x7a|\x7b|\x7c|\x7d|\x7e|\x8a|\x8b|\x8c|\x8d|\x8e'
	good=b'\x90|\x91|\x92|\x93|\x94|\x95|\x96|\x97|\x98|\x99|\xa0|\xa1|\xa2|\xa3|\xa4|\xa5|\xa6|\xa7|\xa8|\xa9|\xaa|\x9a|\x9b|\x9c|\x9d|\x9e'
	def add_pref(s):
		return special+s.group(0)
	t=add_pref;
	s=re.sub(weird,special,s)
	s=re.sub(good,add_pref,s)
	s=re.sub(bad,b'',s)
	s=re.sub(bad2,b'',s)
	s=re.sub(bad3,b'',s)
	s=re.sub(bad4,b'',s)
	s=re.sub(bad5,b'',s)
	s=re.sub(b'\xd7\xd7',b'\xd7',s)
	return s


def questions_not_exist_check(page):
	check = page.evaluate_xpath('//p[@class="content"]//text()')
	if(len(check)==0):
		return True
	return False


def add_type_triple(page):
	page.set_object_type_resource()
	page.add_triple(page.get_url(),'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
		'http://jbs.technion.ac.il/ontology/Question')

def no_quotation_marks(s):
	s = re.sub('"','',s)
	return s

nqm=no_quotation_marks


def add_title_triple(page):
	page.set_object_type_string()
	page.set_object_func(0)
	page.set_predicate('http://jbs.technion.ac.il/ontology/title')
	page.set_object_query('//h1/text()')
	page.add_triple_object_xpath(page.get_url())
	a=annoying_hebrew_issues(page.triples[len(page.triples)-1]['object'].encode('utf-8','ignore')).decode('utf-8','ignore')
	page.triples[len(page.triples)-1]['object']=a

def add_rabbi_triple(page):
	page.set_predicate('http://jbs.technion.ac.il/ontology/rabbiName')
	page.set_object_query('//h2/a/text()')
	page.add_triple_object_xpath(page.get_url())
	a=annoying_hebrew_issues(page.triples[len(page.triples)-1]['object'].encode('utf-8','ignore')).decode('utf-8','ignore')
	page.triples[len(page.triples)-1]['object']=a

def add_date_triple(page):
	page.set_predicate('http://jbs.technion.ac.il/ontology/date')
	page.set_object_query('//div[@class="quesDate"]/text()')
	def remove_spaces(s):
		return s.replace('  ','')
	rs = remove_spaces
	page.set_object_func(remove_spaces)
	page.add_triple_object_xpath(page.get_url())	
	a=annoying_hebrew_issues(page.triples[len(page.triples)-1]['object'].encode('utf-8','ignore')).decode('utf-8','ignore')
	page.triples[len(page.triples)-1]['object']=a


def add_question_and_answer_text(page):
	subejct_elements = page.evaluate_xpath('//p[@class="content"]//text()')
	question = ''
	answer = ''
	i=1
	a=u'תשובה:'
	while i < len(subejct_elements) and annoying_hebrew_issues(subejct_elements[i].encode('utf-8','ignore')).decode('utf-8','ignore')!=a:#.encode('utf-8')
		question = question+subejct_elements[i]
		i=i+1
	i=i+1
	while i < len(subejct_elements):
		answer = answer+subejct_elements[i]
		i=i+1
	j=100
	while(j<len(question)):
		if question[j]==' ':
			question=question[:j]+'\n'+question[j+1:]
			j=j+100
		else:
			j=j+1
	j=100
	while(j<len(answer)):
		if answer[j]==' ':
			answer=answer[:j]+'\n'+answer[j+1:]
			j=j+100
		else:
			j=j+1
	page.set_object_func(0)
	page.add_triple(page.get_url(),'http://jbs.technion.ac.il/ontology/questionText',
		no_quotation_marks(question))
	a=annoying_hebrew_issues(page.triples[len(page.triples)-1]['object'].encode('utf-8','ignore')).decode('utf-8','ignore')
	page.triples[len(page.triples)-1]['object']=a	
	page.add_triple(page.get_url(),'http://jbs.technion.ac.il/ontology/answerText',
		no_quotation_marks(answer))
	a=annoying_hebrew_issues(page.triples[len(page.triples)-1]['object'].encode('utf-8','ignore')).decode('utf-8','ignore')
	page.triples[len(page.triples)-1]['object']=a


page = marom.page()
index=1
questions_not_exist = open('questions_not_exist.txt','w')

while index <= 100000:
	page.set_url('http://www.yeshiva.org.il/ask/'+str(index))
	print(index)
	if questions_not_exist_check(page):
		questions_not_exist.write(str(index)+'\n')
		index=index+1
		continue
	
	
	#inserting the question class triple

	add_type_triple(page)

	#geting the title

	add_title_triple(page)

	#rabbi triples

	add_rabbi_triple(page)

	#date triples
	add_date_triple(page)

	#question and answer text - the ugly part
	add_question_and_answer_text(page)


	index=index+1

questions_not_exist.close()
page.turtle('questions_output.txt')



