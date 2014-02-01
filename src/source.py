#main source code

#import functions
try:
	from itertools import izip_longest as izip
	from pylab import *
	import matplotlib.pyplot as plt
	import pickle
	import numpy
	import scipy 
	import matplotlib.cm as cm
	import matplotlib.collections as collections
	from random import randint
	import time
	import os
	import ttest
except: print "Unable to import a module"

#determine correct directory to use
try:
    directoryListing = os.listdir("/media/")
    if 'KINGSTON' in directoryListing:
    	king = '/media/KINGSTON/blocking/gen_data/'
    	king_gra = '/media/KINGSTON/blocking/graphs/'
    	king_dat = '/media/KINGSTON/blocking/data/pkl_files/blocking/'
    elif 'jonathan' in directoryListing:
		king = '/media/jonathan/KINGSTON/blocking/gen_data/'
		king_gra = '/media/jonathan/KINGSTON/blocking/graphs/'
		king_dat = '/media/jonathan/KINGSTON/blocking/data/pkl_files/blocking/'
    elif 'jonny' in directoryListing:
		king = '/media/jonny/KINGSTON/blocking/gen_data/'
		king_gra = '/media/jonny/KINGSTON/blocking/graphs/'
		king_dat = '/media/jonny/KINGSTON/blocking/data/pkl_files/blocking/'

except IOError as err:	print "Cannot import module: " + str(err)

def open_pkl(data_dir,filename,output=False):
	#import pickle formatted data
	try:
		with open(data_dir + filename, 'rb') as pf:
			#assign the dictionary variable f
			f = pickle.load(pf)
			if output == True:
				print 'Loaded file: ' + filename
				print 'From dir:    ' + data_dir
		pf.close()
		return f

	except IOError as err:
		print "File error: " + str(err)

	except pickle.PickleError as perr:
		print "Pickling error: " + str(perr)

def basemap():
	#basemap
	try:
		from mpl_toolkits.basemap import Basemap
		import matplotlib.pyplot as plt
		#import numpy as np

		# use low resolution coastlines.
		map = Basemap(boundinglat=22,lon_0=0,projection='npaeqd',resolution='l')

		# draw coastlines, country boundaries, fill continents.
		map.drawcoastlines(linewidth=0.25)
		map.drawcountries(linewidth=0.25)
		map.fillcontinents(color='white')

		# draw the edge of the map projection region (the projection limb)
		map.drawmapboundary()

		plt.title('Contours of countries for orthographic basemap')
		plt.show()
		return 0

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def quantile(array,kth=2,type=3):
	#calculate the quantile of a given data set
	try:
		#order the array
		array = sorted(array)
		lngth = len(array)
		factor = float(kth)*float(lngth)/float(type)
		#calculate quartile value
		return array[int(factor)-1]
	except ValueError as err:
		print "Value Error: " + str(err)

def blocking(s_dir,s_name,out_dir,start=1958,end=2002,q_type=3,s_type='OSF',high=True,opt=False):
	#produce a list of files of high/low blocking
	#example: source.blocking('/home/loki/mad/green/data/pkl_files/solar_cycle/','OSF.year1675-2010.sf.pkl','../data/')
	try:
		#get options sorted
		if high == True:
			quant,high = 2,'high'
		if high == False:
			quant,high = 1,'low'
		with open(str(out_dir)+high+'_'+str(s_type)+'.year'+str(start)+'-'+str(end)+'.sf.pkl','wb') as output:
			years = []
			count = []
			f = open_pkl(s_dir.strip(),s_name.strip())

			#options for TSI/OSI
			if s_type == 'OSF':
				i = 1675
				for element in f['sf']:
					count.append(i)
					i += 1
				f = f['sf'][start-count[0]:-(count[-1]-end)]
				line = quantile(f,quant)
				i = 1958
				for value in f:
					if high == 'high':
						if value >= line:
							years.append(1)
						else: years.append(0)
					else:
						if value <= line:
							years.append(1)
						else: years.append(0)
					if opt == True: print years[-1],i
					i += 1
			pickle.dump(years,output)
			output.close()
		return years

	except ValueError as err:
		print "Value Error: " + str(err)

def sol_ext(dat_dir=king+'data/',dat_name='_OSF.year1958-2002.sf.pkl',l_name='era40_blocking_thpv2.list',high='high',q_type='OSI',count=3):
	#now read the main file list in triplets and write to file a list of files for high/low solar ready to be contour plotted
	try:
		#import pickle types
		if high != 'high': high = 'low'

		#import files
		with open(dat_dir + high + dat_name,'rb') as pf:
			#assign the dictionary variable f
			times = pickle.load(pf)
			pf.close()
		with open(dat_dir + l_name,'rb') as lf:
			files = []
			for line in lf.readlines():
				files.append(str(line.strip()))
			lf.close()

		# #process write to output file
		with open(dat_dir + high +'_'+ l_name, 'wb') as output:
			count = 0
			for value in times:
				i = 1
				while(i <= 3 and value == 1):
					output.write(str(files[count])+"\n")
					i += 1
					count += 1
				if value == 0: count += 3
			output.close()
		return 0

	except ValueError as err:
		print "Value Error: " + str(err)

def read_list(filelist=king+'era40_blocking_thpv2.list',directory=king_dat,numpy=True):
	#read a list of files and outputs a data array of the average data values
	try:
		if numpy != True:
			count = 0
			with open(filelist) as files:
				dat = []
				tmp = []
				flength = len(files.readlines())
				files.seek(0)
				for file in files.readlines():
					f = open_pkl(directory.strip(),file.strip())
					#generate first values
					if count == 0:
						dat = []
						for lat in range(0,len(f['lat']['lat'])):
							tmp = []
							for lon in range(0,len(f['lon']['lon'])):
								tmp.append(float(sum(f['b'][lat][lon][0]))/float(len(f['b'][0,0,0])*flength))
							dat.append(tmp)
						count = 1	
						continue
					#append the subsequent values
					for lat in range(0,len(f['lat']['lat'])):
						for lon in range(0,len(f['lon']['lon'])):
							dat[lat][lon] += float(sum(f['b'][lat][lon][0]))/float(len(f['b'][0,0,0])*flength)
				files.close()
			return dat
		if numpy == True:
			with open(filelist) as files:
				files.seek(0)
				flength = len(files.readlines())
				files.seek(0)
				count = 0
				for file in files.readlines():
					f = open_pkl(directory.strip(),file.strip())
					if count == 0:
						data = zeros(f['b'].shape[0:2])
					f['b'].shape = (len(f['b']),len(f['b'][0]),len(f['b'][0,0,0]))
					data = data + np.array(np.mean(f['b'],axis=2))
					count += 1
				data = data/float(flength)
				files.close()
			return data

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def test_plot():
	#test contour plot
	alpha = 0.7
	phi_ext = 2 * pi * 0.5

	def flux_qubit_potential(phi_m, phi_p):
		return 2 + alpha - 2 * cos(phi_p)*cos(phi_m) - alpha * cos(phi_ext - 2*phi_p)

	phi_m = linspace(0, 2*pi, 100)
	phi_p = linspace(0, 2*pi, 100)
	X,Y = meshgrid(phi_p, phi_m)
	Z = flux_qubit_potential(X, Y)

	fig, ax = plt.subplots()
	print Z
	p = ax.pcolor(X/(2*pi), Y/(2*pi), Z, cmap=cm.RdBu, vmin=abs(Z).min(), vmax=abs(Z).max())
	cb = fig.colorbar(p, ax=ax)
	fig.savefig("test.png")

def contour(output=king_gra,high=True,blk=True,type='thpv2',col=False):
	#2D contour plot
	try:
		opt = []
		if type == 'thpv2': v = 'v'
		elif type == 'Z500': v = 'p'
		if blk == True:
			#get coordinate values
			data_xy = open_pkl(king_dat,'era40.gga'+v+'.year-2002.month-01.b.'+type+'_003.duration_ge_5_day.pkl')
			lon,lat = data_xy['lon']['lon'],data_xy['lat']['lat']
			X,Y = meshgrid(lon,lat)
			opt.append(X)
			opt.append(Y)
			if high == True:
				out = 'high_blk_cont_'+type+'.png'
				Z = read_list(king+'high_era40_blocking_'+type+'.list',king_dat)
			elif high == False:
				out = 'low_blk_cont_'+type+'.png'
				Z = read_list(king+'low_era40_blocking_'+type+'.list',king_dat)
			#align data points to set prime meridian at 0 longitude
			for lon in Z:
				lon+=lon;del lon[-(len(lon)/4):-1],lon[0:len(lon)/3],lon[-1]
			opt.append(array(Z))
			#plot coordinates
			# if col == False:
			# 	contour(array(Z))
			if col != False:
				fig, ax = plt.subplots()
				p = ax.pcolor(X, Y, array(Z), cmap=cm.RdBu, vmin=array(Z).min(), vmax=array(Z).max())
				cb = fig.colorbar(p, ax=ax)
				fig.savefig(output+out)
		return opt

	except ValueError as err:
		print "Value Error: " + str(err)

def stdata(datalist=king+'era40_blocking_thpv2.list',directory=king_dat,monthly='thpv2',daily=False,total=False,numpy=True):
	try:
		#METHOD: 25/11/13
		#
		#from a list of data, this reads in data values for each entry preserving time values
		#conditionally, compute time averages for each section
		#returns a data array of several dimensions
		#
		if numpy == True:
			count = 0 #counter for by-monthly averages > 1
			with open(datalist) as files:
				npdata = []
				tmp = []
				flength = len(files.readlines())
				files.seek(0)
				for file in files.readlines():
					f = open_pkl(directory.strip(),file.strip())
					#generate initial values
					if count == 0:
						npdata = zeros((flength,f['b'].shape[0],f['b'].shape[1]))
					f['b'].shape = (len(f['b']),len(f['b'][0]),len(f['b'][0,0,0]))
					npdata[count] = npdata[count] + np.array(np.mean(f['b'],axis=2))
					count += 1
				files.close()
			#consider for different monthly averages
			if monthly == 'thpv2':
				# print "0"
				# print npdata[0]
				# print "1"
				# print npdata[1] 
				# print "2"
				# print npdata[2]
				# print (npdata[0][0][0]+npdata[1][0][0]+npdata[2][0][0])/float(3)
				npdata.shape = (int(flength/3),3,npdata.shape[1],npdata.shape[2])
				npdata = np.mean(npdata,axis=1)
				# print "fin",npdata.shape
				# print npdata[0]
			return npdata
		if numpy != True:
			count = 0
			with open(datalist) as files:
				data = []
				tmp = []
				if total == True:
					flength = len(files.readlines())
					files.seek(0)
				for file in files.readlines():
					f = open_pkl(directory.strip(),file.strip())
					#generate initial values
					if count == 0:
						dat = []
						for lat in range(0,len(f['lat']['lat'])):
							tmp = []
							for lon in range(0,len(f['lon']['lon'])):
								if daily == False:
									if monthly == 1:
										tmp.append(sum(f['b'][lat][lon][0])/(len(f['b'][0,0,0])))
									else: return data
								else: return data
							dat.append(tmp)
					data.append(array(dat))
				files.close()

			return np.array(data)

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def average(data,hist=False):
	try:
		#################################################################
		# METHOD: 5/12/13												#
		#																#
		# take an array of data in form [month][lat][lon] 				#							#
		# compute average blocking frequency for each lat lon point 	#
		# then difference from all-time data (climatological data) 		#
		# plot this difference using basemap and compare to Woolings 	#
		# Note: this function returns blocking frequency in the form 	#
		#		[lat][lon] 												#
		#																#
		#################################################################
		if hist == False:
			#to be completed since this may be a slow method
			return 0
		else:
			opt = []
			diff = data[1][1] - data[1][0]
			opt.append(diff)
			#find midpoints
			midpt = []
			for value in data[1]:
				if value == data[1][-1]: break
				midpt.append(float(value)+float(diff)/float(2))
			#evaluated multiplied sum
			midpt = [a*b for a,b in zip(list(data[0]),list(midpt))]
			opt.append(sum(midpt))
			opt.append(midpt)
			opt.append(sum(midpt)/sum(data[0]))
			#output difference and mean of histogram
			return opt
		
	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def diff_test(test,clim,sum=False):
	try:
		#Example:
		#METHOD: 25/11/13
		#
		#generate a b_diff field from an array (=b_HS-b_clim)
		test,clim = np.array(test),np.array(clim)
		diff = test-clim
		return diff

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def ttest():
	try:
		
		pass

	except ValueError as err:
		print "Value Error: " + str(err)

def sig_test(monte=True,ttest=False,list_name='era40_blocking_thpv2.list',list_dir=king,data_dir=king_dat,high=True,month='thpv2',trials=1000,cutoff=0.95):
	try:
		# determining whether list is high/low solar data
		hh = 'high'
		if high != True: hh = 'low'
		# filepath of solar data list
		name = list_dir+hh+'_'+list_name
		# extracting data to arrays
		solar_data = stdata(name,directory=data_dir,monthly=month)
		all_data = stdata(list_dir+list_name,directory=data_dir,monthly=month)
		# blocking frequency of hig/low solar and climatological blocking frequency
		clim = read_list(list_dir+list_name,data_dir)
		b_hls = read_list(name,data_dir)
		# test statistic
		diff = np.array(b_hls)-np.array(clim)
		# test1 = zeros(array(all_data[0]).shape)
		# region1,region2 = all_data, solar_data
		# print region1
		# region1.shape = (20,96,45)
		# # region2.shape = (20,96,15)
		# # test = np.array()
		# print region1
		if ttest == True:
			test1 = zeros(array(all_data[0]).shape)
			region1,region2 = all_data, solar_data
			region1.shape = (20,96,45)
			# region2.shape = (20,96)
			# print scipy.stats.ttest_ind(region[0][, b, axis=0, equal_var=True)
		# monte carlo bootstrap method for determining a lat/lon array of significances
		if monte == True:
			# generate trial values for analysis
			for trial in range(trials):
				#generate len(solar_data) random years and initial zero array
				test = zeros(array(all_data[0]).shape)
				for i in range(len(solar_data)):
					year = randint(0,len(solar_data)-1)
					# check for correct shape, exit is not
					if all_data[year].shape != (20,96):
						exit(0)
					# append each randomly generated year to test array
					test += all_data[year]
				# first trial condition
				if trial == 0:	
					# generate statistic
					values = test/len(solar_data)-clim
					# values = np.array(diff_test(test/len(solar_data),clim))
					# reshape for concatenation
					values.shape = (len(values),len(values[0]),1)
				# same method as above for subsequent trials
				elif trial != 0:
					tmp = np.array(test/len(solar_data)-clim)
					# tmp = np.array(diff_test(test/len(solar_data),clim))
					tmp.shape = (len(values),len(values[0]),1)
					# concatenate arrays to form final array
					values = np.concatenate((values,tmp),2)
			# reshape difference array for concatenation
			diff.shape = (len(values),len(values[0]),1)
			# return the index within each element of the array that will sort the values
			values = np.concatenate((values,diff),2).argsort().argsort()
			# account for odd behaviour for when both are zero
			# for lat in range(len(values)):
			# 	for lon in range(len(values[lat])):
			# 		if values[lat][lon][-1] == trials:# and diff[lat][lon][0] == 0:
			# 			values[lat][lon][-1] = trials/2
					# if lat == 19:
						# print values[19][lon][-1],diff[19][lon]
			# isolate index that the difference array will need when sorting
			sig = np.delete(values,s_[:-1],2)
			# reshape array to lat/lon style
			sig.shape = (len(values),len(values[0]))
			# transform indices into probabilities
			sig = sig.astype(float)/float(trials)

			# # alternate method - I consider this to be incorrect but did produce okay graphs
			# sig = (values == trials).nonzero()[-1] # sig = sig.astype(float)/float(trials)		#generate an array of 1s and 0s depending if in range of two tailed significance #values <lower limit
			lower = (1-cutoff)/2
			opt = - (sig - (1+lower)).astype(int)
			#values > upper limit
			opt = opt + (sig + (1-cutoff)/2).astype(int)
			print opt.shape
			return opt
		if ttest == True: return 0


	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

a = np.array(range(-100,102,2))/float(100)
print a

def diff(high=True,type='thpv2',v='v',graph=True,filled=False,sig=False,monthly=1,trials=1000,cutoff=0.95):

	#################################################################
	# METHOD: 25/11/13												#
	#																#
	# take high/low solar data 										#
	# compute average blocking frequency for each lat lon point 	#
	# then difference from all-time data (climatological data) 		#
	# plot this difference using basemap and compare to Woolings 	#
	# Note: this function returns the difference data 				#
	#																#
	#################################################################
		
	try:
		#read in x-y data
		opt = []
		data_xy = open_pkl(king_dat,'era40.gga'+v+'.year-2002.month-01.b.'+type+'_003.duration_ge_5_day.pkl')
		Lon,Lat = data_xy['lon']['lon'],data_xy['lat']['lat']
		Lon = np.append(Lon,360+Lon[0])
		#print Lon
		X,Y = meshgrid(Lon,Lat)
		opt.append(X)
		opt.append(Y)
		# #read in data
		if high == True:
			data = read_list(king+'high_era40_blocking_'+type+'.list',king_dat)
		elif high != True:
			data = read_list(king+'low_era40_blocking_'+type+'.list',king_dat)
		clim = read_list(king+'era40_blocking_'+type+'.list',king_dat)
		#checks of data read in
		if len(data) != len(clim) or len(data[0]) != len(clim[0]):
			print "Error: Array lengths don't match\nData: "+str(len(data)),str(len(data[0]))+"\nClim: "+str(len(clim)),str(len(clim[0]))
			return 0
		#compute difference array
		diff = zeros(shape=(len(data),len(data[0])+1))
		test = []
		for lat in range(0,len(data)):
			for lon in range(0,len(data[0])):
				diff[lat][lon] =  -clim[lat][lon] + data[lat][lon]
		#final value for diff
		for lat in range(0, len(data)):
			diff[lat][-1] = -clim[lat][0] + data[lat][0]
		opt.append(diff)

		if sig == True:	
			try: 
				regions = sig_test(list_name='era40_blocking_thpv2.list',list_dir=king,data_dir=king_dat,high=high,trials=1000,cutoff=0.90)
				extra = regions[:,0]
				extra.shape = (regions[:,0].shape[0],1)
				regions = np.concatenate((regions,extra),1)
			except ValueError as err:	print "Value Error: " + str(err)

		if graph == True:
			from mpl_toolkits.basemap import Basemap
			import matplotlib.pyplot as plt

			# use low resolution coastlines.
			fig = plt.figure()
			map = fig.add_subplot()
			map = Basemap(boundinglat=Lat[-1],lon_0=0,projection='npaeqd',resolution='l',round=True)
			lon,lat = np.array(opt[0]),np.array(opt[1])
			x,y = map(lon,lat)

		 	# draw coastlines, country boundaries, fill continents.
			map.drawcoastlines(linewidth=0.25)
			map.drawcountries(linewidth=0.25)

			# draw the edge of the map projection region (the projection limb)
			map.drawmapboundary()
			#if sig == True: map.fill()
			if sig == True: map.contourf(x,y,regions,1,cmap=cm.gray_r,alpha=0.5)
			if filled == False:	map.contour(x,y,np.array(opt[2]))#,colors='k')
		 	elif filled == True: 
				map.contour(x,y,np.array(opt[2]),a,linestyles='solid',colors='black')
		 		map.contourf(x,y,np.array(opt[2]),10)
	 		#map.pcolormesh(...)
		return opt

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def histogram():
	# A histogram
	n = np.random.randn(100000)
	fig, axes = plt.subplots(1, 2, figsize=(12,4))

	axes[0].hist(n)
	axes[0].set_title("Default histogram")
	axes[0].set_xlim((min(n), max(n)))

	axes[1].hist(n, cumulative=True, bins=50)
	axes[1].set_title("Cumulative detailed histogram")
	axes[1].set_xlim((min(n), max(n)));
	return 0

#outputs
diff(high=False,filled=False,sig=True)
#basemap()
#read_list(numpy=True)
#stdata(monthly='thpv2')
#print monte(high=True)
