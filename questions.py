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

def questions_not_exist_check():
	check = page.evaluate_xpath('//p[@class="content"]//text()')
	if(len(check)==0):
		return True
	return False


def type_triple():
	page.triples.append({})
	page.triples[len(page.triples)-1]['subject']='<'+page.get_url()+'>'
	page.triples[len(page.triples)-1]['predicate']='<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
	page.triples[len(page.triples)-1]['object']='<http://jbs.technion.ac.il/resource/Question>'

def title_triple():
	page.set_subject_query('//h1/text()')
	page.set_predicate('<http://jbs.technion.ac.il/resource/title>')
	page.set_object_query('/text()')
	def f(param):
		return '<'+page.get_url()+'>'
	func = f
	def f2(str):
		return '"'+str+'"'
	func2 = f2
	page.set_subject_func(func)
	page.set_object_func(func2)
	page.create_triples()
	page.triples[len(page.triples)-1]['object']=some_encoding_issues(page.triples[len(page.triples)-1]['object'])


def rabbi_triple():
	page.set_subject_query('//h2/a/text()')
	page.set_predicate('<http://jbs.technion.ac.il/resource/rabbiName>')
	page.set_object_query('/text()')

	def f3(str):
		return '"'+str+'"'
	func3 = f3
	page.set_object_func(func3)
	page.create_triples()
	page.triples[len(page.triples)-1]['object']=some_encoding_issues(page.triples[len(page.triples)-1]['object'])


def date_triple():
	page.set_subject_query('//div[@class="quesDate"]/text()')
	page.set_predicate('<http://jbs.technion.ac.il/resource/date>')
	page.set_object_query('/text()')

	def f4(str):
		return '"'+str+'"'
	func4 = f4
	page.set_object_func(func4)
	page.create_triples()
	page.triples[len(page.triples)-1]['object']=some_encoding_issues(page.triples[len(page.triples)-1]['object'])




def question_and_answer_text():
	subejct_elements = page.evaluate_xpath('//p[@class="content"]//text()')
	question = ''
	answer = ''
	i=1
	a=u'תשובה:'
	while i < len(subejct_elements) and some_encoding_issues(subejct_elements[i])!=a:#.encode('utf-8')
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
	page.triples.append({})
	page.triples[len(page.triples)-1]['subject']='<'+page.get_url()+'>'
	page.triples[len(page.triples)-1]['predicate']='<http://jbs.technion.ac.il/resource/questionText>'
	page.triples[len(page.triples)-1]['object']='"'+some_encoding_issues(question)+'"'

	page.triples.append({})
	page.triples[len(page.triples)-1]['subject']='<'+page.get_url()+'>'
	page.triples[len(page.triples)-1]['predicate']='<http://jbs.technion.ac.il/resource/answerText>'
	page.triples[len(page.triples)-1]['object']='"'+some_encoding_issues(answer)+'"'

def boring_technical_stuff():
	arr = []
	j=0
	for i in range(len(page.triples)):
		if page.triples[i]['object'] != '<http://jbs.technion.ac.il/resource/Question>':
			arr.append(page.triples[i]['object'])
			page.triples[i]['object']='"zz'+str(j)+'zz"'
			j=j+1

	page.turtle('questions_output.txt')

	with open('questions_output.txt','r') as f:
		text = f.read()
	f.close()
	for i in range(len(arr)):
		s = '"zz'+str(i)+'zz"'
		text = re.sub(s,arr[i],text)
	f = open('questions_output.txt','w')
	f.write(text.encode('utf-8'))
	f.close()
	for line in fileinput.input('questions_output.txt', inplace=True):
		print(string.replace(line,'foaf:','jbr:').rstrip()) 
	f.close()

page = marom.page()
index=1
questions_not_exist = open('questions_not_exist.txt','w')
count = open('page_count.txt','w')

while index <= 100:
	page.set_url('http://www.yeshiva.org.il/ask/'+str(index))
	count.write(str(index)+'\n')
	if questions_not_exist_check():
		questions_not_exist.write(str(index)+'\n')
		index=index+1
		continue
	
	
	#inserting the question class triple
	type_triple()

	#geting the title

	title_triple()

	#rabbi triples

	rabbi_triple()

	#date triples
	date_triple()

	#question and answer text - the ugly part
	question_and_answer_text()


	index=index+1

questions_not_exist.close()
count.close()

boring_technical_stuff()


