import numpy as np
from pylab import *
from open import read_list

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

def diff1(king,king_dat,output,high=True,type='thpv2',v='v',monte=False,sttest=True,tcrit=0.87,graph=True,filled=False,sig=False,monthly=1,trials=1000,cutoff=0.90):

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
		from open import open_pkl
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
			#generate listname
			listnm = 'era40_blocking_'+str(type)+'_high_blk'
			stype = 'high'
		elif high != True:
			data = read_list(king+'low_era40_blocking_'+type+'.list',king_dat)
			#generate listname
			listnm = 'era40_blocking_'+str(type)+'_low_blk'
			stype = 'low'
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
				from sig_test import sig_test
				regions = sig_test(list_name='era40_blocking_thpv2.list',list_dir=king,monte=monte,sttest=sttest,tcrit=tcrit,data_dir=king_dat,high=high,trials=1000,cutoff=cutoff)
				extra = regions[:,0]
				extra.shape = (regions[:,0].shape[0],1)
				regions = np.concatenate((regions,extra),1)
			except ValueError as err:	print "Value Error: " + str(err)

		if graph == True:
			#generate output filename
			if monte == True: sgtype = 'monte'
			if sttest == True: sgtype = 'ttest'
			output = str(output)+'blk'+str(listnm)+str(sgtype)+str(int(100*(1-cutoff)+1))+'.png'

			from mpl_toolkits.basemap import Basemap
			import matplotlib.pyplot as plt

			# use low resolution coastlines.
			fig,ax = plt.subplots()
			# fig = plt.figure()
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
			if filled == False:	
				a = np.array(range(-100,102,2))/float(100)
				p = map.contour(x,y,np.array(opt[2]),a,colors='k')
		 	elif filled == True: 
		 		a = np.array(range(-100,102,2))/float(100)
				c = map.contour(x,y,np.array(opt[2]),10,linestyles='solid',colors='black')
		 		p = map.contourf(x,y,-np.array(opt[2]),10,cmap=cm.RdBu,vmin=np.array(opt[2]).min(),vmax=np.array(opt[2]).max(),alpha=0.5,)
		 		cb = fig.colorbar(p, ax=ax)
		 		t = ax.set_title('blk'+stype+'-clim')
		 	if sig == True:
		 		# masking the array 
				regions = np.ma.array(regions)
				interior = regions < 0.5
				regions[interior] = np.ma.masked
				s = map.contourf(x,y,regions,1,cmap=cm.gray_r)
				t = ax.set_title('blk'+str(stype)+'-clim (sig '+str(int(100*(1.0-cutoff)+1))+'%)')
			fig.savefig(str(output))
		return opt

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

def diff(king=0,king_dat=0,output=0,arr=Falsehigh=True,type='thpv2',v='v',monte=False,sttest=True,tcrit=0.87,graph=True,filled=False,sig=False,monthly=1,trials=1000,cutoff=0.90):

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
		if arr != True
		from open import open_pkl
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
		from open import stdata
		all_data = stdata('[DIR]/era40_blocking_thpv2.list',directory='/media/jonathan/KINGSTON/blocking/data/pkl_files/blocking/',monthly='thpv2')
		from solar import years
		yrs = np.array(years()['SCmin'])-1957

		if high == True:
			yrs = np.array(years()['SCmax'])-1957
			data = np.mean(all_data[yrs],axis=0)
			# data = read_list(king+'high_era40_blocking_'+type+'.list',king_dat)
			#generate listname
			listnm = 'era40_blocking_'+str(type)+'_high_blk'
			stype = 'high'
		elif high != True:
			yrs = np.array(years()['SCmin'])-1957
			data = np.mean(all_data[yrs],axis=0)
			# data = read_list(king+'low_era40_blocking_'+type+'.list',king_dat)
			#generate listname
			listnm = 'era40_blocking_'+str(type)+'_low_blk'
			stype = 'low'
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
				from sig_test import sig_test
				regions = sig_test(list_name='era40_blocking_thpv2.list',list_dir=king,monte=monte,sttest=sttest,tcrit=tcrit,data_dir=king_dat,high=high,trials=1000,cutoff=cutoff)
				extra = regions[:,0]
				extra.shape = (regions[:,0].shape[0],1)
				regions = np.concatenate((regions,extra),1)
			except ValueError as err:	print "Value Error: " + str(err)

		if graph == True:
			#generate output filename
			if monte == True: sgtype = 'monte'
			if sttest == True: sgtype = 'ttest'
			output = str(output)+'blk'+str(listnm)+str(sgtype)+str(int(100*(1-cutoff)+1))+'.png'

			from mpl_toolkits.basemap import Basemap
			import matplotlib.pyplot as plt

			# use low resolution coastlines.
			fig,ax = plt.subplots()
			# fig = plt.figure()
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
			if filled == False:	
				a = np.array(range(-100,102,2))/float(100)
				p = map.contour(x,y,np.array(opt[2]),a,colors='k')
		 	elif filled == True: 
		 		a = np.array(range(-100,102,2))/float(100)
				c = map.contour(x,y,np.array(opt[2]),10,linestyles='solid',colors='black')
		 		p = map.contourf(x,y,-np.array(opt[2]),10,cmap=cm.RdBu,vmin=np.array(opt[2]).min(),vmax=np.array(opt[2]).max(),alpha=0.5,)
		 		cb = fig.colorbar(p, ax=ax)
		 		t = ax.set_title('blk'+stype+'-clim')
		 	if sig == True:
		 		# masking the array 
				regions = np.ma.array(regions)
				interior = regions < 0.5
				regions[interior] = np.ma.masked
				s = map.contourf(x,y,regions,1,cmap=cm.gray_r)
				t = ax.set_title('blk'+str(stype)+'-clim (sig '+str(int(100*(1.0-cutoff)+1))+'%)')
			fig.savefig(str(output))
		return opt

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)
