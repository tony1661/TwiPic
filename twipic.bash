#!/bin/bash

		webpage=$(curl -s -I  $1) 
		echo $1

		imgurl=$(echo $webpage | egrep -o "(http|https)://[a-zA-Z][a-zA-Z0-9]*.([a-zA-Z_0-9]+.)+[a-zA-Z_]*(/[a-zA-Z_0-9.]*)*([/A-Za-z0-9]*)/?" | rev | cut -c 2- | rev)
		wget -N -O tpages/1.html "$(echo $imgurl)" 1> NUL 2> NUL
		pic=$(cat tpages/1.html | egrep -o "(http|https)://[a-zA-Z][a-zA-Z0-9]*.([a-zA-Z_0-9]+.)+[a-zA-Z_]*(/[a-zA-Z_0-9.]*)*([/A-Za-z0-9]*)\.(jpg|png)" | sed -n '4p')
		picname=$(echo $pic | egrep -o "[A-Za-z0-9_-]*\.(jpg|png)")
		if [ ! -f tpics/$picname ]; then
			cd tpics
			wget $(echo $pic)  1> NUL 2> NUL
			sleep 3
			echo $(echo $pic) "Downloaded...."
			cd ..
		else
			echo "File Exists"
		fi
