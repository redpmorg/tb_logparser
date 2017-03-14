r = range(35, 51)
l = list(r)
i = 4
print(l)
def reduce_rec(_l, last):
	print(last)
	if len(_l) > last:
		if _l[last-1] + i >= _l[last]:
			del _l[last]
			reduce_rec(_l, last)
		reduce_rec(_l, last+1)
reduce_rec(l, 1)
print(l)