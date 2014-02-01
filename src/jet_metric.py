try:
	import os
	directoryListing = os.listdir("/media/")
	if '[insert directory signifyer here]' in directoryListing:
		king =
		king_gra =
		king_jet =
		king_dat =
		king_xfwnl =
		king_xfwnh =
		king_xhjjb =
		king_xhjjc =
		king_xhjjd =
		king_sol =
		king_list = 

except IOError as err:	print "Cannot import module: " + str(err)

import numpy as np

#find leap years

years = range(1958,2002)

days = 0
for year in years:
	if year % 4 == 0:
		if year % 100 == 0 and year % 400 != 0:
			days += 365
			continue
		days += 366
	else: days += 365

value = 6806

def jet(dat_dir=king_dat,strength='jsi',Atlantic=True,start=1957,end=2001,a=305,b=90,compress=False,select=True,mnmx='SCmax'):
	# want to select high/low solar
	if select == True:
		from solar import years
		yrs = years()[mnmx]

	# call data in
	from open import open_pkl
	strength = strength
	Atlantic = True
	if Atlantic == True:
		sea = 'Atlantic'
	elif Atlantic == False:
		sea = 'Pacific'
	# use import pickle extractor
	database = open_pkl(dat_dir,'era40.year'+str(start)+'-'+str(end)+'.month11-15.'+str(strength)+'.JI_001.'+str(sea)+'.pkl')
	data = database[str(database['info']['name'])]
	data.shape = data.shape[-1]

	# compress days into months, first get the days database
	days = database['time']['day_of_year']

	# firstly create a loop for specific number of years
	# identify empty data array	
	jdat = np.array([])

	# empty arrays
	jet = np.array([])
	tmp = np.array([])

	# counters
	i,dat=1,0

	# check if first year is leap year
	year = start
	last = b
	if year % 4 == 0:
		if year % 100 == 0 and year % 400 != 0:	
			last = b+1

	# loop over days
	sum = 0
	for day in days:
		tmp = np.append(tmp,data[dat])
		if i == len(days): 
			# final append before breaking
			if compress == True:
				jet = np.append(jet,np.mean(tmp))
			else:
				if year in yrs:
					jet = np.append(jet,tmp)
			tmp = np.array([])
			break
		if day == last:
			#once the winter end has been reached append this data
			sum += len(tmp)
			if compress == True:
				jet = np.append(jet,np.mean(tmp))
			else:
				if year in yrs:
					jet = np.append(jet,tmp)
			tmp = np.array([])
			# check if next year will be leap year
			year += 1
			last = b
			if (year+1) % 4 == 0:
				if (year+1) % 100 == 0 and (year+1) % 400 != 0:	pass
				else: last = b+1
		i += 1
		dat += 1
	return jet

a = jet(compress=False,mnmx='SCmin')

#plotting and analysing the data

#having got the jet data, produce a simple plot of it

def plots(SC='SCmax',compress=False,select=True,two_hist=True,wrttime=False,hist=False,strength='jsi',start=1957,end='2001',sig=False,sea='Atlantic'):
	# get data
	data = jet(strength=strength)

	# plot data wrt time to compare to blocking cycle
	import matplotlib.pyplot as plt
	from solar import years

	yrs = np.array(years()[SC])-start
	all_yrs = np.array(range(1957,2002))-start

	if wrttime == True:
		fig = plt.figure()
		x = all_yrs+start#linspace(0, 5, 10)
		y = data
		axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
		axes.plot(x, y, 'r')
		axes.set_xlabel('time (winters)')
		axes.set_ylabel(strength)
		axes.set_title('Jet '+strength+' wrt time');
		fig.savefig(king_gra+'jet_'+strength+'_wrt_time')

	if two_hist == True:
		if select == False:
			from open import open_pkl
			database = open_pkl(king_dat,'era40.year'+str(start)+'-'+str(end)+'.month11-15.jsi.JI_001.'+str(sea)+'.pkl')
			sdata = database[str(database['info']['name'])]
			sdata.shape = sdata.shape[-1]
			database = open_pkl(king_dat,'era40.year'+str(start)+'-'+str(end)+'.month11-15.jli.JI_001.'+str(sea)+'.pkl')
			ldata = database[str(database['info']['name'])]
			ldata.shape = ldata.shape[-1]			
		elif compress == False:
			sdata = jet(strength='jsi',mnmx=SC)
			ldata = jet(strength='jli',mnmx=SC)
		else:
			sdata = jet(strength='jsi',compress=True)
			ldata = jet(strength='jli',compress=True)
		from matplotlib.colors import LogNorm
		fig = plt.figure()
		# plt.subplots
		# plt.scatter(ldata,sdata)
		plt.hist2d(ldata,sdata, bins=40, cmap='Greens', norm=LogNorm())
		ax = plt.gca()
		ax.set_xlabel('jli')
		ax.set_ylabel('jsi')
		plt.title("Jet jsi v jli for "+SC)
		plt.colorbar()
		# plt.xlim(-15, 15)
		# plt.ylim(-15, 15)
		plt.show()
		fig.savefig(king_gra+'jet_jsi_v_jli_'+SC)

	if hist == True:
		# plot a histogram of values based on high/low solar
		max = np.array(years()['SCmax'])-start
		min = np.array(years()['SCmin'])-start
		# years()
		# # print years
		# print data[yrs]
		# print np.mean(data[yrs]),np.mean(data[max]),np.mean(data[min])
		plt.subplots()
		plt.hist(data[all_yrs],20)
		plt.subplots()
		plt.hist(data[max],20)	
		plt.subplots()
		plt.hist(data[min],20)

	#try a ttest for the means
	if sig == True:
		import sig_test
		data.shape = (data.shape[-1],1,1)
		print sig_test.ttest(data,data[min],tcrit=1.34)[0][0]
plots(SC='SCmax',strength='jli')
