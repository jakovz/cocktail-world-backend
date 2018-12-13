#!/usr/bin/python

import urllib
import urllib2
import json
import zlib

url = ''
values = {'name' : 'Yuval',
		  'location' : 'Tel Aviv'}

data = urllib.urlencode(values)
req = urlib2.Request(url, data)  # Need to change this to work on python 3
response = urllib2.urlopen(req)
the_page = response.read()
