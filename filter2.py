import os, heapq
from operator import itemgetter
from datetime import datetime

export = dict()

def filter_times_by_id(file_path, export):
	f = open(file_path, 'r')
	for line in f:
		data = line.split(',')
		if data[8] != 'points':
			if data[7] not in export:
				if int(data[8]) < 15: #Unlikely to get more than 15 points in 10 minutes
					#store data
					export[data[7]] = {'timestamp': data[1],'dayofweek':data[4], 'time':data[5], 'top': int(data[9])}
			elif int(data[9]) == 1:
				export[data[7]]['top'] = 1;
	return export

#
###### Functions that produced the charts for          ######
###### http://hnews.phpfogapp.com/welcome/time_to_post ######
#

def probability_matrix(export):
	days = dict();
	for key, row in export.iteritems():
		if row['dayofweek'] in days:
			if row['time'] in days[row['dayofweek']]:
				days[row['dayofweek']][row['time']]['all'] += 1
				if row['top'] == 1:
				 	days[row['dayofweek']][row['time']]['top'] += 1
			else:
				days[row['dayofweek']][row['time']] = {'top':row['top'], 'all': 1}
		else:
			days[row['dayofweek']] = dict()
			days[row['dayofweek']][row['time']] = {'top':row['top'], 'all': 1}
	return probabilities(days)
	
def probabilities(days):
	week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	for day in week:
		print_str = 'var '+day+'=['
		for time, data in sorted(days[day].iteritems(), key=itemgetter(0)):
			print_str += '['+time.replace(":", ".")+', '+str(data['top']/(data['all'] + 0.0)*100)+'],'
		print print_str + ']'
		print '\n';

#
###### Functions that sort data by unique times and  ######
###### identifies the times with the highest ratios  ######
#
		
def highest_times(export):
	times = dict();
	for key, row in export.iteritems():
		if row['timestamp'] in times:
			times[row['timestamp']]['all'] += 1
			if row['top'] == 1:
				times[row['timestamp']]['top'] += 1
		else:
			times[row['timestamp']] = {'top':row['top'], 'all': 1.0}
	ratios = dict((key, {'ratio': value['top']/value['all']*100, 'top': value['top'], 'all': value['all']}) for key, value in times.iteritems())
	return ratios

def largest_ratios(num, export, tolerance):#tolerance, for eliminating cases where all < n
	ratios = highest_times(export)
	filter_dict = dict((key, value['ratio']) for key, value in ratios.iteritems() if value['all'] > tolerance)
	toptimes = heapq.nlargest(num,filter_dict, key = lambda k: filter_dict[k])
	
	for t in toptimes:
		print datetime.fromtimestamp(int(t)/1000).strftime('%m-%d-%Y %H:%M:%S')
		print 'Number of articles posted: '+str(ratios[t]['all'])
		print 'Number that made it to top: '+str(ratios[t]['top'])
		print 'Ratio: '+str(ratios[t]['ratio'])
		print ''



for r,d,f in os.walk("./"):
	for files in f:
		if files.endswith(".csv"):
			export = filter_times_by_id(files, export)
			#print export
#print probability_matrix(export)
largest_ratios(5, export, 10)