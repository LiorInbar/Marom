#!/usr/bin/env python
# -*- coding: utf-8 -*-

import triples_creator_3

import urllib
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET
from rdflib import Graph
import string
import fileinput
import re
import sys




def questions_not_exist_check():
	page = urllib.urlopen('http://www.yeshiva.org.il/ask/'+str(index)).read()
	tree = etree.HTML(page)
	subejct_elements = tree.xpath('//p[@class="content"]//text()')
	if(len(subejct_elements)==0):
		return True
	return False

def bad_pages_check():
	page = urllib.urlopen('http://www.yeshiva.org.il/ask/'+str(index)).read()
	tree = etree.HTML(page)
	subejct_elements = tree.xpath('//p[@class="content"]//text()')
	if subejct_elements[0]!=u'שאלה:':
		return True
	return False

def type_triple():
	questions.triples.append({})
	questions.triples[len(questions.triples)-1]['subject']='<http://www.yeshiva.org.il/ask/'+str(index)+'>'
	questions.triples[len(questions.triples)-1]['predicate']='<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>'
	questions.triples[len(questions.triples)-1]['object']='<http://jbs.technion.ac.il/resource/Question>'

def title_triple():
	questions.set_subject_query('//h1/text()')
	questions.set_predicate('<http://jbs.technion.ac.il/resource/title>')
	questions.set_object_query('/text()')
	def f(param):
		return '<http://www.yeshiva.org.il/ask/'+str(index)+'>'
	func = f
	def f2(str):
		return '"'+str+'"'
	func2 = f2
	questions.set_subject_func(func)
	questions.set_object_func(func2)
	questions.create_triples()

def rabbi_triple():
	questions.set_subject_query('//h2/a')
	questions.set_predicate('<http://jbs.technion.ac.il/resource/rabbi>')
	questions.set_object_query('/@href')

	def f3(str):
		return '<'+str+'>'
	func3 = f3
	questions.set_object_func(func3)
	questions.create_triples()



def question_and_answer_text():
	page = urllib.urlopen('http://www.yeshiva.org.il/ask/'+str(index)).read()
	tree = etree.HTML(page)
	subejct_elements = tree.xpath('//p[@class="content"]//text()')
	question = ''
	answer = ''
	i=1
	a=u'תשובה:'
	while subejct_elements[i]!=a:#.encode('utf-8')
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
	questions.triples.append({})
	questions.triples[len(questions.triples)-1]['subject']='<http://www.yeshiva.org.il/ask/'+str(index)+'>'
	questions.triples[len(questions.triples)-1]['predicate']='<http://jbs.technion.ac.il/resource/question_text>'
	questions.triples[len(questions.triples)-1]['object']='"'+question+'"'

	questions.triples.append({})
	questions.triples[len(questions.triples)-1]['subject']='<http://www.yeshiva.org.il/ask/'+str(index)+'>'
	questions.triples[len(questions.triples)-1]['predicate']='<http://jbs.technion.ac.il/resource/answer_text>'
	questions.triples[len(questions.triples)-1]['object']='"'+answer+'"'

def boring_technical_stuff():
	arr = []
	j=0
	for i in range(len(questions.triples)):
		if questions.triples[i]['object'] != '<http://jbs.technion.ac.il/resource/Question>':
			arr.append(questions.triples[i]['object'])
			questions.triples[i]['object']='"zz'+str(j)+'zz"'
			j=j+1

	questions.turtle('questions_output.txt')

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
		print(string.replace(line,'foaf:','jbo:').rstrip()) 
	f.close()

questions = triples_creator_3.page()
index=1
questions_not_exist = open('questions_not_exist.txt','w')
bad_pages = open('bad_pages.txt','w')

while index <= 100:
	questions.set_url('http://www.yeshiva.org.il/ask/'+str(index))

	if questions_not_exist_check():
		questions_not_exist.write(str(index)+'\n')
		index=index+1
		continue

	if bad_pages_check():
		bad_pages.write(str(index)+'\n')
		index=index+1
		continue

	#inserting the question class triple
	type_triple()

	#geting the title

	title_triple()

	#rabbi triples

	rabbi_triple()

	#question and answer text - the ugly part
	question_and_answer_text()


	index=index+1

questions_not_exist.close()
bad_pages.close()

boring_technical_stuff()

'''nt = open('test2.txt','w')
nt.write(questions.triples[1]['object'].encode('utf-8'))'''

