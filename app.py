__author__  = "Tiberiu Andrei Lepadatu"
__email__   = "tiberiulepadatu15@gmail.com"
__license__ = "None"

import sys, os
import utils as U

inputfile = open(os.path.join('./data/tests', 'test0.log'), 'r')
lines = inputfile.readlines()  #this is list type
_interval = 1
_start = None
_end = None
_success_filter = ""
mylist = U.convert_mylist(lines)

# the main function for the script, called by the shell
if __name__ == "__main__":
	if len(sys.argv) > 2:
		sys.argv.pop(0) #pop out the name of application file
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
			else:
				sys.tracebacklimit = 0
				print ("\n\n")
				raise ValueError("I don't recognize {} argument(s)!" \
					.format(arg))


newlist = U.filter_by_date(mylist, _start, _end, _interval)

# newlist_len = len(newlist)

import itertools
from operator import itemgetter
from collections import Counter
import math

newlist = sorted(newlist, key=itemgetter('datetime'))
for k, v in itertools.groupby(newlist, key=itemgetter('datetime')):
	v = sorted(v, key=itemgetter('request'))
	for i, vv in itertools.groupby(v, key=itemgetter('request')):
		# tc = len(list(v))
		success_tc = sum(Counter(d['status'] \
			for d in list(v) if d['status'][0] == '2').values())
		success_c = sum(Counter(d['status'] \
			for d in list(vv) if d['status'][0] == '2').values())
		print (k, i,  "%.2f" % float(success_c/success_tc*100))

		

# c = Counter(itemgetter('request')(vl))
	# for i in v:
		# print (i.get('request'))

# print (groups)
# print (uniquekey)
# print (newlist)


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