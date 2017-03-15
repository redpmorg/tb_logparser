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
args_tuple = zip(sys.argv[::2], sys.argv[1::2])
for arg, value in args_tuple:
	if arg == "--interval":
		_interval = int(value)
	elif arg == "--start":
		_start = value
	elif arg == "--end":
		_end = value
	elif arg == "--success":
		_success_filter = value

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

newlist = U.filter_by_date(mylist, _start, _end)

import itertools
from operator import itemgetter
from collections import Counter, defaultdict
import math, datetime as dt

rl = []
interval = dt.timedelta(minutes=_interval)
_k = itemgetter('datetime')
_kk = itemgetter('request')
newlist = sorted(newlist, key=_k)
for k, v in itertools.groupby(newlist, key=_k):
	v = sorted(v, key=_kk)
	for i, vv in itertools.groupby(v, key=_kk):
		tv = list(vv).copy()
		tvv = list(tv).copy()
		success_c = sum(Counter(d['status'] \
			for d in list(tv) if d['status'][0] == '2').values())
		success_tc = len(list(tvv))

		# this will pass tests from 0 to 3 -> 40%
		# print (k, _interval, i, "%.2f" % float(success_c/success_tc*100))

		rl.append({"datetime": k, "request": i, "success": success_c, "total": success_tc})

# print (rl)

# debugger
# import pdb; pdb.set_trace()

_dt = rl[0]['datetime']
_success_cnt = rl[0]['success']
_request = rl[0]['request']
_total = rl[0]['total']
compare = [_dt]
result = {}
result[_dt] = {}
result[_dt][_request] = {}
result[_dt][_request][_dt] = {"total": _total, "success": _success_cnt}

for r in rl[1:]:
	dt = r['datetime']
	req = r['request']
	succ = r['success']
	tot = r['total']
	#
	if U.dt_decode(compare[0]) + interval >= U.dt_decode(dt):
		if req in result[compare[0]]:
			if dt in result[compare[0]][req]:
				result[compare[0]][req][dt]['success'] = succ + result[dt][req]['success']
				result[compare[0]][req][dt]['total'] = tot + result[dt][req]['total']
			else:
				# result[compare[0]][req] = {}
				result[compare[0]][req][dt] = {'success': succ, 'total': tot}
		else:
			# result[compare[0]] = {}
			result[compare[0]][req] = {}
			result[compare[0]][req][dt] = {'success': succ, 'total': tot}
	else:
		result[dt] = {}
		result[dt][req] = {}
		result[dt][req][dt] = {"success": succ, "total": tot,}
		compare = [dt]

print (result.items())

# for k in list(result.items()):
# 	print (k[0], k[1])


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