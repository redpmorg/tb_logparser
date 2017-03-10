"""
In 'code' we will spoke only in english. If romanians invented the computers the situation have been different ...
"""

__author__  = "Tiberiu Andrei Lepadatu"
__email__   = "tiberiulepadatu15@gmail.com"
__license__ = "None"


import sys, os
import utils as U


inputfile = open(os.path.join('./data/tests', 'test0.log'), 'r')

lines = inputfile.readlines()  #this is list type

mylist = U.convert_mylist(lines)


## didactic block only --- removing in production
# print "\n\n"
# print ("mylist type is:" + str(type(mylist)))
# print "\n\n"
# print ("mylist items types are:" + str(type(mylist[0])))
# print "\n\n"
# print mylist
# print "\n\n"
# print mylist[0]
# print "\n\n"
### endblock

req = U.split_request(mylist[0])
## didactic block only --- removing in production
# print req
# print req['endpoint']
# print "\n\n"
### endblock

## didactic block only --- removing in production
#
d =  U.datetime_convert(mylist[0])
# print "date converted"
# print d
# print d.day
# print d.month
# print d.year
# print d.hour
# print d.minute

#I think this it should need it in reporting :)
# print "datetime encoded :: " + U.datetime_encode(d)
# print "datetime decoded :: " + str(U.datetime_decode('2016-07-31T09:46'))

# print "\n\n"
### endblock


# the main function for the script, called by the shell
if __name__ == "__main__":
# 	# check number of arguments (including the command name)
	if len(sys.argv) > 1:
		sys.argv.pop(0) #pop out the name of application file

		args_tuple = zip(sys.argv[::2], sys.argv[1::2])
		_interval = 1
		_start = None
		_end = None
		_success_filter = None
		for arg, value in args_tuple:
			# sorry! pyhton doesn;t have switch statement. it can be implemented with lambda functions but I don't like it
			if arg == "--interval":
				_interval = value
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
				print "\n\n"
				raise ValueError("I don't recognize {} argument(s)!" \
					.format(arg))

	else:
		sys.tracebacklimit = 0
		print "\n\n"
		raise ValueError("Please provide some arguments!")


newlist = U.filter_by_date(mylist, _start, _end)




print newlist

# outputfile = open('my_log.log', 'w')
# outputfile.truncate() # wipe the file
# for line in newlist:
# 	l = U.datetime_encode(U.datetime_convert(line))
# 	l += " "
# 	l += str(_interval)
# 	l += " "
# 	l += line['request']
# 	l += " "
# 	l += line['status'] #this should be changed
# 	l += "\n"
# 	outputfile.write(l)
# outputfile.close()