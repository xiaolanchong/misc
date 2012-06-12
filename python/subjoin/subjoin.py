# -*- coding: utf-8 -*-

import sys
import codecs
import bisect
import re
import datetime
from operator import itemgetter

eol = "\r\n"

def readSubtitles(subFile):
	subs = []
	startTime = None
	time = ''
	text = ''
	for line in subFile.readlines():
		line = line.strip()
		m = re.match('(\d\d):(\d\d):(\d\d),(\d\d\d) --> ' \
					 '(\d\d):(\d\d):(\d\d),(\d\d\d)', line)
		if m is not None:
			time = line
			text = ''
			startTime = datetime.timedelta(hours=int(m.group(1)),
										   minutes=int(m.group(2)),
										   seconds=int(m.group(3)),
										   milliseconds=int(m.group(4)))
		elif line == '' and len(time) != 0:
			subs.append([startTime, time, text])
			text = ''
			time = ''
		elif line != '':
			if text != '':
				text += eol
			text += line
		else:
			print("darn", line)
	return sorted(subs, key=itemgetter(0))

if len(sys.argv) != 3:
	print(sys.argv[0], ": <target subs> <eng subs>")
	sys.exit()
	
mainSubFile = codecs.open(sys.argv[1], "r", "utf-8")
auxSubFile = open(sys.argv[2], "r")

outFile = codecs.open("out.srt", "w", "utf-8")
mainSubs = readSubtitles(mainSubFile)
auxSubs = readSubtitles(auxSubFile)

startTimes = list(map(lambda x: x[0], mainSubs))
for startTime, timeLine, text in auxSubs:
	pos = bisect.bisect(startTimes, startTime)
	if pos > -1:
		mainSubs[pos-1][2] += ' ' + text

num = 1
#outFile.write(str(codecs.BOM_UTF8))
for _,time,text in mainSubs:
	outFile.write(str(num))
	outFile.write(eol)
	outFile.write(time)
	outFile.write(eol)
	outFile.write(text)
	outFile.write(eol + eol)
	num += 1
	