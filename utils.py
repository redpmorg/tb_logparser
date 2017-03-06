import re   #regular expresion
import datetime as dt, time as tm

def split_request(request):
	r = request['request'].split()
	return {
		'request': r[0],
		'endpoint': r[1],
		'protocol': r[2] 
		}

def get_status(request):
	return request['status']

def convert_mylist(lines):
	### 
	# boss, bellow parts are for Nginx log. 
	# I don't have Apache here 
	# So if is not working you should rebuild it.
	# Sorry, But you are "tatic" in regex :)
	# Note that: r is from raw, ?P it is an identifier
	# propper to python because py can load perl and vice-versa

	parts = [
	    r'\S+',                   # host %h
	    r'\S+',                             # indent %l (unused)
	    r'\S+',			                    # user %u
	    r'\[(?P<datetime>.+)\]',            # time %t
	    r'"(?P<request>.+)"',               # request "%r"
	    r'(?P<status>[0-9]+)',              # status %>s
	    r'\S+',                   			# size %b (careful, can be '-')
	    r'".*"',               				# referer "%{Referer}i"
	    r'".*"',                 			# user agent "%{User-agent}i"
	]
	pattern = re.compile(r'\s+'.join(parts) + r'\s*\Z')

	## didactic block only --- removing in production
	#print "\n\n"
	#print pattern.pattern
	### endblock

	#let's make our input list
	mylist = list()
	for line in lines:
		m = pattern.match(line)
		if m:
			mylist.append(m.groupdict())
	return mylist

 	
## param: datetime - log string datetime
## retrun datetime object ex: 2017-02-22 18:45
def datetime_convert(request):
	r = request['datetime'][:-6]
	return dt.datetime.strptime(r, '%d/%b/%Y:%I:%M:%S')

## param: datetime - converted datetime
## retrun string ex: 2017-02-22T18:45
def datetime_encode(datetime):
	return str(datetime).replace(" ", "T")[:-3]
	
## param: string ex: 2017-02-22T18:45
## retrun datetime object ex: 2017-02-22 18:45
def datetime_decode(datetime):
	datetime = datetime.replace("T", " ") 
	return dt.datetime.strptime(datetime, '%Y-%m-%d %I:%M')


def filter_by_date(mylist, start, end):
	newlist = list()
	def filter_my_data(x):
		if datetime_convert(x) > datetime_decode(start) \
			and datetime_convert(x) <  datetime_decode(end):
				#just update the request and datetime values. Is not propper place to do it here, but will be chenged in future#
				x['request'] = split_request(x)['endpoint']
				newlist.append(x)
		return newlist

	map(lambda x: filter_my_data(x), mylist)

	newlist = sorted(newlist, key=lambda x: (datetime_convert(x), x['request']))
	return newlist