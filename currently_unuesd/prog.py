#!/usr/bin/python
import urllib
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET

page = urllib.urlopen("http://www.cs.technion.ac.il/people/faculty/index.html").read()
tree = etree.HTML(page)
lines = [line.rstrip('\n').split() for line in open('input.txt')]
output =  open('output.txt', 'w')
for l in lines:
    paths = []
    res = []
    n=0 
    for k in l:
    	if k=='$':
    		n=n+1
    if n==2:
    	paths.append(l[0])
    	paths.append(l[2])
    	res =  tree.xpath(paths[0])
    	for d in range(len(res)):
    		e = 4
    		s = ''
    		while e < len(l):
    			if l[e] == '@':
    				s = s + ' ' + tree.xpath(paths[0])[d]
    			elif l[e] == '@@':
    				s = s + ' ' + tree.xpath(paths[0]+paths[1])[d]
    			else:
    				s = s + ' ' + l[e]
    			e = e+1
    		output.write(s+'\n')
    elif n==1:
    	paths.append(l[0])
    	res =  tree.xpath(paths[0])
    	for d in range(len(res)):
    		e = 2
    		s = ''
    		while e < len(l):
    			if l[e] == '@':
    				s = s + ' ' + tree.xpath(paths[0])[d]
    			else:
    				s = s + ' ' + l[e]
    			e = e+1
    		output.write(s+'\n')	   
