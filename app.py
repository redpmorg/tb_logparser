#!/usr/bin/python3

__author__  = "Tiberiu Andrei Lepadatu"
__email__   = "tiberiulepadatu14@gmail.com"
__license__ = "None"

import sys, os, utils as U, fileinput, re

_interval = 1
_start = None
_end = None
_success_filter = None

# inputfile = open(os.path.join('./data/tests', value), 'r')
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


from operator import itemgetter
from collections import Counter, defaultdict
from functools import reduce
import math, datetime as dt, itertools


newlist = U.filter_by_date(mylist, _start, _end, _interval)
_k = itemgetter('datetime')
_kk = itemgetter('request')
_interval = dt.timedelta(minutes=_interval)
newlist = sorted(newlist, key=_k)

# # print (newlist)

# x = [{"datetime":k[0],
# 		"request":k[1],
# 		"status": k[2],
# 		"total": len(list(v))
# 		} for k, v in itertools.groupby(newlist, lambda x: (x['datetime'], x['request'], x['status']))]
# # print (x)
# dic = dict()
# def check_me(s, acc=None):

# 	print (s)
# d = [k for k in map(check_me, x)]
# print(d)


# for k, v in itertools.groupby(x, key=itemgetter('datetime')):
	# print (k, len(list(v))) 

# for k, v in itertools.groupby(newlist, key=itemgetter('request', 'status')):
# 	print (k, len(list(v))) 

# martors = sorted({U.dt_decode(d['datetime']) for d in newlist})
# def reduce_martors(_martors, c):
# 	if(len(_martors) > c):
# 		if _martors[c-1] + _interval >= _martors[c]:
# 			del _martors[c]
# 			reduce_martors(_martors, c)
# 		reduce_martors(_martors, c+1)
# reduce_martors(martors, 1)

# result_list = []
# for d in newlist:
# 	for m in martors:
# 		if U.dt_decode(d['datetime']) <= m+_interval:
# 			result_list.append({"g_datetime": U.dt_encode(m), "request": d['request'], "stat": d['status'], "datetime": d['datetime']})

for d, v in itertools.groupby(sorted(result_list, key=itemgetter('g_datetime')), key=itemgetter('request')):
	_v = list(sorted(v, key=_kk)).copy()
	print(d)
	for i, vv in itertools.groupby(v, key=kk):
		tc = len(list(v))
		tv = list(vv).copy()
		tvv = list(tv).copy()
		success_c = sum(Counter(d['status'] for d in list(tv) if d['status'][0] == '2').values())
		success_tc = len(list(tvv))
	print (k, list(v), "\n")
	for kk, vv in v:
		print (k, list((v)), "\n")
		print (k, _interval, i, "%.2f" % float(success_c/success_tc*100))

		# ddiff = U.dt_decode(semn) - U.dt_decode(vv['datetime'] + dt.timedelta(minutes=_interval)):

		result_list.append({"datetime": k, "request": i, "success": success_c, "total": success_tc})


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