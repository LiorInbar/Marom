#!/usr/bin/python
import urllib
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET

def create_triples( url, format, output, querry1,  querry2 = '' ):
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    res1 =  tree.xpath(querry1)
    for c in range(len(res1)):
        s=''
        d=0
        while d < len(format):
            if(d<len(format)-1):
                if (format[d] == '@') and (format[d+1] != '@'):
                    s = s + res1[c]
                elif (format[d] == '@') and (format[d+1] == '@'):
                    res2 = tree.xpath(querry1+'['+str(c)+']'+querry2)
                    if res2:
                        s = s + res2[0]
                    else:
                        s = s + ' '
                    d=d+1
                else:
                    s = s + format[d]
            else:
                if (format[d] == '@'):
                    s = s + res1[c]
                else:
                    s = s + format[d]
            d=d+1
        output.write(s+'\n')

def html_elements_list(url, querry):
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    res =  tree.xpath(querry)
    return res

def html_elements_two_lists(url, querry1, querry2):
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    list1 =  tree.xpath(querry1)
    list2 = []
    for c in range(len(list1)):
        res2 = tree.xpath(querry1+'['+str(c)+']'+querry2)
        if res2:
            list2.append(res2[0])
        else:
            list2.append(' ')
    list = [list1, list2]      

    return list


def create_triples_from_list( url, format, output, list1, list2 = [] ):
 
    for c in range(len(list1)):
        s=''
        d=0
        while d < len(format):
            if(d<len(format)-1):
                if (format[d] == '@') and (format[d+1] != '@'):
                    s = s + list1[c]
                elif (format[d] == '@') and (format[d+1] == '@'):
                    s = s + list2[c]
                    d=d+1
                else:
                    s = s + format[d]
            else:
                if (format[d] == '@'):
                    s = s + list1[c]
                else:
                    s = s + format[d]
            d=d+1
        output.write(s+'\n')

def create_triples_from_list_and_querrys( url, format, output, list, querry1, querry2):
 
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    res1 =  tree.xpath(querry1)
    for c in range(len(res1)):
        s=''
        d=0
        while d < len(format):
            if(d<len(format)-1):
                if (format[d] == '@') and (format[d+1] != '@'):
                    s = s + res1[c]
                elif (format[d] == '@') and (format[d+1] == '@'):
                    res2 = tree.xpath(querry1+'['+str(c)+']'+querry2)
                    if res2:
                        s = s + res2[0]
                    else:
                        s = s + ' '
                    d=d+1
                else:
                    s = s + format[d]
            else:
                if (format[d] == '@'):
                    s = s + res1[c]
                else:
                    s = s + format[d]
            d=d+1
        output.write(s+'\n')

def create_triples_2( url, format, output, base_querry, querry1, func1,  querry2, func2):
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    if querry1!=0:
        res1 =  tree.xpath(base_querry)
        for c in range(len(res1)):
            s=''
            d=0
            while d < len(format):
                if(d<len(format)-1):
                    if (format[d] == '@') and (format[d+1] != '@'):
                        res2 = tree.xpath(base_querry+'['+str(c+1)+']'+querry2)
                        if(func1!=0):
                            s = s + func1(res1[c])
                        else:
                            s = s + res1[c]
                    elif (format[d] == '@') and (format[d+1] == '@'):
                        res2 = tree.xpath(querry1+'['+str(c+1)+']'+querry2)
                        if res2:
                            if(func2!=0):
                                s = s + func2(res2[0])
                            else:
                                s = s + res2[0]             
                        else:
                            s = s + ' '
                        d=d+1
                    else:
                        s = s + format[d]
                else:
                    if (format[d] == '@'):
                        if(func1!=0):
                            s = s + func1(res1[c])
                        else:
                            s = s + res1[c]
                    else:
                        s = s + format[d]
                d=d+1
            output.write(s+'\n')

def create_triples_3( url, format, output, base_querry, querry1, func1,  querry2, func2):
    page = urllib.urlopen(url).read()
    tree = etree.HTML(page)
    if querry1!=0:
        base =  tree.xpath(base_querry)
        for c in range(len(base)):
            s=''
            d=0
            while d < len(format):
                if(d<len(format)-1):
                    if (format[d] == '@') and (format[d+1] != '@'):
                        res1 = tree.xpath(base_querry+'['+str(c+1)+']'+querry1)
                        if(res1):
                            if(func1!=0):
                                s = s + func1(res1[0])
                            else:
                                s = s + res1[0]
                    elif (format[d] == '@') and (format[d+1] == '@'):
                        res2 = tree.xpath(base_querry+'['+str(c+1)+']'+querry2)                       
                        if res2:
                            if(func2!=0):
                                s = s + func2(res2[0])
                            else:
                                s = s + res2[0]             
                        else:
                            s = s + ' '
                        d=d+1
                    else:
                        s = s + format[d]
                else:
                    if (format[d] == '@'):
                        res1 = tree.xpath(base_querry+'['+str(c+1)+']'+querry1)
                        if(func1!=0):
                            s = s + func1(res1[c])
                        else:
                            s = s + res1[c]
                    else:
                        s = s + format[d]
                d=d+1
            output.write(s+'\n')