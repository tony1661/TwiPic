#!C:\Python27\python.exe
import re
import pprint
import urllib2
import urllib
import subprocess
import sys, time
import PIL

import textwrap

from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from twython import Twython
from xml.dom import minidom



#Variable declaration
id = 0
transfer = 0
urlregex = "(http|https)://[t]\.[co]*(/[a-zA-Z_0-9.]*)/?"
picregex = "(http|https)://pbs[.]twimg[.]com(/[a-zA-Z_0-9.-]*/)([a-zA-Z0-9.-_]*)[.](jpg|png)[:]large"
picnameregex = "[a-zA-Z0-9-_]*[.](jpg|png)"
searchregex = "(http|https)://[t]\.[co]*(/[a-zA-Z_0-9.]*)"
handle = "^@[A-Za-z_0-9]* "

#Function Declaration
def overlay(text, file, profilepic):
	text = re.sub(handle, '', text)
	text = re.sub(urlregex, '', text)
	print text
	picname = "temp.png"
	urllib.urlretrieve(profilepic, "ppics/%s" % picname)
	twipic = Image.open(file)
	foreground = Image.open("transparent.png")
	blackback = Image.open("background.png")
	w = blackback.size[0]
	h = blackback.size[1]
	twipic_width = twipic.size[0]
	twipic_height = twipic.size[1]
	nw = w*0.8
	nh = h*0.85
	nw = int(nw)
	nh = int(nh)
	blackback.paste(twipic, (((w-twipic_width)/2), ((nh-twipic_height)/2)))
	blackback.paste(foreground, (0, int(h*0.85)), foreground)
	blackback.paste(foreground, (400, int(h*0.85)), foreground)
	blackback.paste(foreground, (800, int(h*0.85)), foreground)
	blackback.save(file)
	picarea = w*h
	picarea = picarea/2
	picarea = picarea*0.1
	print picarea
	blackback = Image.open(file)
	white = Image.open("ppics/white.png").resize((120, 120))
	foreground = Image.open("ppics/temp.png").resize((100, 100))

	pw = blackback.size[0]
	ph = blackback.size[1]
	pw = w*0.05
	ph = h*0.84
	pw = int(pw)
	ph = int(ph)
	blackback.paste(white, (int(w*0.045), int(h*0.83)))
	blackback.paste(foreground, (pw, ph))
	blackback.save(file)
	img=Image.open(file)
	font = ImageFont.truetype("/usr/share/fonts/truetype/arista.ttf",45)
	draw = ImageDraw.Draw(img)
	text = textwrap.wrap(text,50)
	if len(text) == 0:
		draw.text((int(w*0.2), int(h*0.9)),text,"#FFFFFF",font=font)
	elif len(text) == 1:
		draw.text((int(w*0.2), int(h*0.9)),text[0],"#FFFFFF",font=font)
	elif len(text) == 2:
		draw.text((int(w*0.2), int(h*0.88)),text[0],"#FFFFFF",font=font)
		draw.text((int(w*0.2), int(h*0.92)),text[1],"#FFFFFF",font=font)
	else:
		draw.text((int(w*0.2), int(h*0.86)),text[0],"#FFFFFF",font=font)
		draw.text((int(w*0.2), int(h*0.90)),text[1],"#FFFFFF",font=font)
		draw.text((int(w*0.2), int(h*0.94)),text[2],"#FFFFFF",font=font)
	draw = ImageDraw.Draw(img)
	img.save(file)
	print "Waiting..."
	time.sleep(1)

def grep(data, regex):
	match = re.search(regex, data)
	if match != None:
		return match.group(0)


######################################################################################
###########################           MAIN START           ###########################
######################################################################################

t = Twython(app_key="NrNZ8RhqUPBNIIj3YvPhZW3j3",
            app_secret="uK0r77j92JvIIK4i6NujCoRhHUoQHfeF3V346lDciV0XqXGes1",
            oauth_token="34105126-rHyDJNCTwRUsFXCyfmBUmVrnZrI1WanMVnh0uZ2yo",
            oauth_token_secret="PKYPTwmTrHGLvmngU4maT1RPWr0EGvfLz6d5PGbJY")

while True:
	id = transfer
	if id != 0:
		mentions = t.get_mentions_timeline(since_id='%d' % id)
		for g in mentions:
			userarray = g['user']
			entities = g['entities']
			try:
				media = entities['media'][0]
				picurl = media['media_url']
				ppic = userarray['profile_image_url']
				tweet = g['text']
				print tweet
				id = g['id']
				if id > transfer:
					transfer = id
				picname = grep(picurl, picnameregex)
				urllib.urlretrieve(picurl, "tpics/%s" % picname)
				overlay(tweet, "tpics/%s" % picname, ppic)
			except KeyError:
				print "No Picture detected..."
	elif id == 0:
		mentions = t.get_mentions_timeline()
		for g in mentions:
			#pprint.pprint(mentions)
			userarray = g['user']
			entities = g['entities']
			try:
				media = entities['media'][0]
				picurl = media['media_url']
				ppic = userarray['profile_image_url']
				tweet = g['text']
				print tweet
				id = g['id']
				if id > transfer:
					transfer = id
				print id
				picname = grep(picurl, picnameregex)
				urllib.urlretrieve(picurl, "tpics/%s" % picname)
				overlay(tweet, "tpics/%s" % picname, ppic)
			except KeyError:
				print "No Picture detected..."
	print "Refreshing in 5 Minutes..."
	time.sleep(600)
	#id = search(id)


