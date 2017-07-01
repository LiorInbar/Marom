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



def some_encoding_issues(text):
	return re.sub(b'\xc3\x97\xc2',b'\xd7',unicode(text).encode('utf-8')).decode('utf-8')

def questions_not_exist_check(page):
	check = page.evaluate_xpath('//p[@class="content"]//text()')
	if(len(check)==0):
		return True
	return False


def add_type_triple(page):
	page.set_object_type_resource()
	page.add_triple(page.get_url(),'http://www.w3.org/1999/02/22-rdf-syntax-ns#type',
		'http://jbs.technion.ac.il/ontology/Question')

def add_title_triple(page):
	page.set_object_type_string()
	page.set_object_func(0)
	page.set_predicate('http://jbs.technion.ac.il/ontology/title')
	page.set_object_query('//h1/text()')
	page.add_triple_object_xpath(page.get_url())


def add_rabbi_triple(page):
	page.set_predicate('http://jbs.technion.ac.il/ontology/rabbiName')
	page.set_object_query('//h2/a/text()')
	page.add_triple_object_xpath(page.get_url())


def add_date_triple(page):
	page.set_predicate('http://jbs.technion.ac.il/ontology/date')
	page.set_object_query('//div[@class="quesDate"]/text()')
	page.add_triple_object_xpath(page.get_url())	



def add_question_and_answer_text(page):
	subejct_elements = page.evaluate_xpath('//p[@class="content"]//text()')
	question = ''
	answer = ''
	i=1
	a=u'תשובה:'
	while i < len(subejct_elements) and subejct_elements[i]!=a:#.encode('utf-8')
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
	page.add_triple(page.get_url(),'http://jbs.technion.ac.il/ontology/questionText',
		question)
	page.add_triple(page.get_url(),'http://jbs.technion.ac.il/ontology/answerText',
		answer)
	

def boring_technical_stuff():
	arr = []
	j=0
	for i in range(len(page.triples)):
		if page.triples[i]['object'] != '<http://jbs.technion.ac.il/ontology/Question>':
			arr.append(page.triples[i]['object'])
			page.triples[i]['object']='"zz'+str(j)+'zz"'
			j=j+1

	page.turtle('questions_output20000_25000.txt')

	with open('questions_output20000_25000.txt','r') as f:
		text = f.read()
	f.close()
	for i in range(len(arr)):
		s = '"zz'+str(i)+'zz"'
		text = re.sub(s,arr[i],text)
	f = open('questions_output20000_25000.txt','w')
	f.write(text)
	f.close()
	for line in fileinput.input('questions_output20000_25000.txt', inplace=True):
		print(line.replace('foaf:','jbo:').rstrip()) 
	f.close()

page = marom.page()
index=20001
questions_not_exist = open('questions_not_exist20000_25000.txt','w')
count = open('page_count.txt','w')

while index <= 25000:
	page.set_url('http://www.yeshiva.org.il/ask/'+str(index))
	count.write(str(index)+'\n')
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
count.close()

boring_technical_stuff()


