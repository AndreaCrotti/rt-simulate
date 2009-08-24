#!/usr/bin/env python
import re, urllib2, os

BASE = "http://dit.unitn.it/~abeni/RTOS/"
PAGE = os.path.join(BASE, "index.html")
DIR = "slides"
res = urllib2.urlopen(PAGE).read()

# Filtering external links
urls = [ url[1:] for url in re.findall(r"\"[a-z0-9A-Z./]*pdf", res)]

for (i, u) in enumerate(urls):
    pdf = os.path.join(BASE, u)
    name = str(i) + "_" + u.split("/")[-1]
    print pdf
    print "fetching ", pdf
    open(os.path.join(DIR, name), 'w').write(urllib2.urlopen(pdf).read())
