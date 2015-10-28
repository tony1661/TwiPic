#!/usr/bin/python
import re
import subprocess
from xml.dom import minidom
import sys, time
import urllib, urllib2


def grep(list):
	regex = "(http|https)://[t]\.[co]*(/[a-zA-Z_0-9.]*)/?"
	#expr = re.compile(regex)
	match = re.search(regex, list)
	if match != None:
		#print "URL: " + match.group(0)
		return match.group(0)
		

#regex = "(http|https)://[a-zA-Z][a-zA-Z0-9]*.([a-zA-Z_0-9]+.)+[a-zA-Z_]*(/[a-zA-Z_0-9.]*)*([/A-Za-z0-9]*)/?"
id = 309789487607726080
i=1
while True:  
	search = "@Tony1661"
	url = "http://search.twitter.com/search.atom?rpp=20&q=%s&since_id=%s" % (search, id)
	xml = urllib.urlopen(url)
	doc = minidom.parse(xml)
	entries = doc.getElementsByTagName("entry")
	if len(entries) > 0:
		
		
		entries.reverse()
		
		for e in entries:
			tweets = ""
			title = e.getElementsByTagName("title")[0].firstChild.data
			pub = e.getElementsByTagName("published")[0].firstChild.data       
			id = e.getElementsByTagName("id")[0].firstChild.data.split(":")[2]
			print id
			name = e.getElementsByTagName("name")[0].firstChild.data.split(" ")[0]
			#print "> " + name + ": \n" + title
			tweets = grep(title)
			if tweets is not None:
				#f = open('tweets','a')
				#f.write(tweets + "\n")
				print ("WRITTEN")
				print tweets
				print "CALLING BASH"
				time.sleep(5)
				child = subprocess.Popen(['bash', '-c', './twipic.bash %s' % (tweets)], stdout = subprocess.PIPE)
			print "\n\n"
			print i
			i=i+1
	print "Sleeping 3 Seconds"
	time.sleep(5)

