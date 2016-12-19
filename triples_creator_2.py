#!/usr/bin/python
import urllib
from lxml import html
from lxml import etree
import xml.etree.ElementTree as ET

def create_triples( url, format, output, querry1, querry2 = '' ):
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
                    s = s + tree.xpath(querry1+'['+c+']'+querry2)
                    d=d+2
                else:
                    s = s + format[d]
            else:
                if (format[d] == '@'):
                    s = s + res1[c]
                else:
                    s = s + format[d]
            d=d+1
        output.write(s+'\n')