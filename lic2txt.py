#!/usr/bin/python

import sys, urllib, hashlib
import elementtree.ElementTree as ET
import sys

# Connect to the Ohloh website and retrieve the account data.

total = 58930
page = 4934
api_key_file = 'ohloh_api_keys.txt'

# read api keys file
api_keys = []
api_file = open(api_key_file)
key_max = 0
for key in api_file:
    api_keys.append(key.strip())
    key_max = key_max + 1
key_num = 0

while page < total:
    api_key = api_keys[key_num]
    params = urllib.urlencode({'api_key': api_key, 'v': 1, 'sort':'id', 'page':page})
    url = "http://www.ohloh.net/projects.xml?%s" % params
    f = urllib.urlopen(url)

    # Parse the response into a structured XML object
    tree = ET.parse(f)

    # Did Ohloh return an error?
    elem = tree.getroot()
    error = elem.find("error")
    if error != None:
        errortxt = ET.tostring(error)
        if 'exceeded its daily access limit' in errortxt and key_num < key_max:
            key_num = key_num + 1
            continue
	print 'Ohloh returned:', errortxt,
	sys.exit()

    for node in elem.findall('result/project'):
	id = int(node.find('id').text)
	url_name = node.find('url_name').text
        if not url_name:
            url_name = 'None'
        url_name = url_name.encode('utf-8')
	name = node.find('name').text.encode('utf-8')
	user_count = int(node.find('user_count').text)
	average_rating = node.find('average_rating').text
	if average_rating is None:
    	    average_rating = 0
	average_rating = float(average_rating)
	licenses = []
	for l in node.find('licenses'):
    	    licenses.append(l.find('name').text.encode('utf-8'))
	if not licenses:
    	    licenses = ['N/A']
	print "%d|%s|%s|%d|%f|%s" % (id, url_name, name, user_count, average_rating, ','.join(licenses))
    page = page + 1
