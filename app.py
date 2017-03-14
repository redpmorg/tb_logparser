#!/usr/bin/python3

__author__  = "Tiberiu Andrei Lepadatu"
__email__   = "tiberiulepadatu14@gmail.com"
__license__ = "None"

import sys, os
import utils as U
import fileinput, re

_interval = 1
_start = None
_end = None
_success_filter = None

# inputfile = open(os.path.join('./data/tests', value), 'r')
# if len(list(sys.argv)) > 2:
	# sys.argv.pop(0) #pop out the name of application file
	# sys.argv.pop(0) #pop out the name of log test file
args_tuple = zip(sys.argv[::2], sys.argv[1::2])
for arg, value in args_tuple:
	if arg == "--interval":
		_interval = int(value)
	elif arg == "--start":
		_start = value
		#do something
	elif arg == "--end":
		_end = value
		#do something else
	elif arg == "--success":
		_success_filter = value
		#do somethign else

del sys.argv[2:]
lines = fileinput.input()

parts = [
    r'\S+',                   							# host %h
    r'\S+',                             				# indent %l (unused)
    r'\S+',			                   				 	# user %u
    r'\[(?P<datetime>.+):[0-9]{2}\s\+[0-9]{4}\]',    	# time %t
    r'"(?P<request>.+)"',       						# request "%r"
    r'(?P<status>[0-9]+)',              				# status %>s
    r'\S+',                   							# size %b (careful, can be '-')
    r'".*"',               								# referer "%{Referer}i"
    r'".*"',                 							# user agent "%{User-agent}i"
]
pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')
mylist = list()
for line in lines:
	m = pattern.match(line)
	if m:
		mylist.append(m.groupdict())

newlist = U.filter_by_date(mylist, _start, _end, _interval)
# newlist_len = len(newlist)

import itertools
from operator import itemgetter
from collections import Counter, defaultdict
import math, datetime as dt

result_list = []
_interval = dt.timedelta(minutes=_interval)
_k = itemgetter('datetime')
_kk = itemgetter('request')
newlist = sorted(newlist, key=_k)
for k, v in itertools.groupby(newlist, key=_k):
	v = sorted(v, key=_kk)
	for i, vv in itertools.groupby(v, key=_kk):
		# tc = len(list(v))
		tv = list(vv).copy()
		tvv = list(tv).copy()
		success_c = sum(Counter(d['status'] \
			for d in list(tv) if d['status'][0] == '2').values())
		success_tc = len(list(tvv))

		# print (k, _interval, i, "%.2f" % float(success_c/success_tc*100))

		# ddiff = U.datetime_decode(semn) - (U.datetime_decode(vv['datetime']) + _interval):

		result_list.append({"datetime": k, "request": i, "success": success_c, "total": success_tc})

# print (result_list)



# outputfile = open('my_log.log', 'w')
# outputfile.truncate() # wipe the file
# for line in newlist:
# 	l = line['datetime']
# 	l += " "
# 	l += str(_interval)
# 	l += " "
# 	l += line['request']
# 	l += " "
# 	l += line['status']
# 	l += "\n"
# 	# outputfile.write(l)
# print (l)
# outputfile.close()