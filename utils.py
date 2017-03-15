import datetime as dt, time as tm, re

def split_request(request):
	r = request['request'].split()
	endpoint = r[1]
	m = re.compile(r'\/.+\.html')
	endpoint = m.match(endpoint)
	return {
		'request': r[0],
		'endpoint': endpoint.group(0),
		'protocol': r[2]
		}

def get_status(request):
	return request['status']

## param: datetime - log string datetime
## retrun datetime object ex: 2017-02-22 18:45:00
def dt_convert(request):
	r = request if type(request) == str else request['datetime']
	r = dt.datetime.strptime(r, '%d/%b/%Y:%H:%M')
	return r

## param: datetime - converted datetime
## retrun string ex: 2017-02-22T18:45
def dt_encode(datetime):
	return str(datetime).replace(" ", "T")

## param: string ex: 2017-02-22T18:45
## retrun datetime object ex: 2017-02-22 18:45:00
def dt_decode(dtime):
	if type(dtime) == str:
		if "T" in dtime:
			dtime = dtime.replace("T", " ")+":00"
	else:
		dtime = str(dtime)
	r =  dt.datetime.strptime(dtime, '%Y-%m-%d %H:%M:%S')
	return r

def filter_by_date(mylist, start, end):
	mylist = sorted(mylist, key=lambda x: (dt_convert(x), x['request'])) # sort by date
	start = dt_decode(
				dt_convert(mylist[0]['datetime'])
				if start == None else start
			)
	end = dt_decode(
				dt_convert(mylist[len(mylist)-1]['datetime']) \
				if end == None else end
				)
	def filter_my_data(x):
		if dt_convert(x) >= dt_decode(start) \
			and dt_convert(x) <= dt_decode(end):
				x['request'] = split_request(x)['endpoint']
				x['datetime'] = dt_encode(dt.datetime.strptime(x['datetime'], '%d/%b/%Y:%H:%M'))[:-3]
				return x

	newlist = filter(None, [map(lambda x: filter_my_data(x), mylist)][0])
	return newlist