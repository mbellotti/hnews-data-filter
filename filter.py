import os

dataset = dict()
export = dict()

#Filters cases so that only the final points total for each article remains
def data_filter(file_path, dataset, export):
	f = open(file_path, 'r')
	for line in f:
		data = line.split(',')
		if data[8] != 'points':
			if data[7] not in dataset or dataset[data[7]] < data[8]:
				#store data
				dataset[data[7]] = data[8]
				export[data[7]] = line
	return export

#Filters cases to one vote articles only
def filter_singles(file_path, dataset, export):
	f = open(file_path, 'r')
	for line in f:
		data = line.split(',')
		if data[8] != 'points':
			if data[7] not in dataset:
				if int(data[8]) == 1:
					#store data
					dataset[data[7]] = int(data[8])
					export[data[7]] = line
			else:
				if int(data[8]) > 1:
					del(dataset[data[7]])
					del(export[data[7]]) 
	return export

def filter_top(file_path, dataset, export):
	#Only articles that have hit the top page
	f = open(file_path, 'r')
	for line in f:
		data = line.split(',')
		if data[8] != 'points':
			if data[7] not in dataset or dataset[data[7]] < data[8]:
				if int(data[9]) == 1:
					#store data
					dataset[data[7]] = int(data[8])
					export[data[7]] = line
	return export

def filter_not_top(file_path, dataset, export):
		#Opposite of the above
		f = open(file_path, 'r')
		for line in f:
			data = line.split(',')
			if data[8] != 'points':
				if data[7] not in dataset or dataset[data[7]] < data[8]:
					if int(data[9]) != 1:
						#store data
						dataset[data[7]] = int(data[8])
						export[data[7]] = line
		return export


def averages_by_day(export):
	#Plain averages by day
	points = dict()
	count = dict()
	for key, value in export.iteritems():
		data = value.split(',')
		if data[4] not in points:
			points[data[4]] = int(data[8])
			count[data[4]] = 1
		else:
			points[data[4]] += int(data[8])
			count[data[4]] += 1
	for key, value in points.iteritems():
		print "Average for %s" % (key)
		print '%d points per article ' % (value/count[key])
		print '%d articles posted' % (count[key])
		print '%d votes in total' % (value)
		print "\n\r"

def averages_by_day_noself(export):
	#removes the point the original poster gives himself for posting
	points = dict()
	count = dict()
	for key, value in export.iteritems():
		data = value.split(',')
		if data[4] not in points:
			points[data[4]] = int(data[8])-1
			count[data[4]] = 1
		else:
			points[data[4]] += int(data[8])-1
			count[data[4]] += 1
	for key, value in points.iteritems():
		print "Average for %s" % (key)
		print '%d points per article ' % (value/count[key])
		print '%d articles posted' % (count[key])
		print '%d votes in total' % (value)
		print "\n\r"

def articles_by_day(export):
	#Calculates average number of articles by day of week
	day = dict()
	days = dict()
	count = dict()
	for key, value in export.iteritems():
		data = value.split(',')
		if data[4] not in count:
			count[data[4]] = 1
			day[data[2]+data[3]+data[6]] = 1
			day[data[4]] = 1
		else:
			if data[2]+data[3]+data[6] not in day:#monthdayyear
				day[data[2]+data[3]+data[6]] = 1
				day[data[4]] += 1
			count[data[4]] += 1
	for key, value in count.iteritems():
		print "Total number of articles posted on %s is %d" % (key, value)
		print 'Average number of articles on %s is %d' % (key, value/day[key])
		print "\n\r"

def points_by_day(export):
	#Calculates average number of points by day of week (not including self votes)
	day = dict()
	days = dict()
	count = dict()
	for key, value in export.iteritems():
		data = value.split(',')
		if data[4] not in count:
			count[data[4]] = int(data[8])-1
			day[data[2]+data[3]+data[6]] = 1
			day[data[4]] = 1
		else:
			if data[2]+data[3]+data[6] not in day:#monthdayyear
				day[data[2]+data[3]+data[6]] = 1
				day[data[4]] += 1
			count[data[4]] += int(data[8])-1
	for key, value in count.iteritems():
		print "Total number of points posted on %s is %d" % (key, value)
		print 'Average number of points on %s is %d' % (key, value/day[key])
		print "\n\r"


for r,d,f in os.walk("./"):
	for files in f:
		if files.endswith(".csv"):
			export = filter_not_top(files, dataset, export)
			#print export
points_by_day(export)