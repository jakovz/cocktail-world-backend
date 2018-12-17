#!/usr/bin/python

import requests
import json
import zlib
from SRC.DBConnection import execute_query

url = ''
values = {'name' : 'Yuval',
		  'location' : 'Tel Aviv'}


a = requests.get()

execute_query()