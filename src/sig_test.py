import numpy as np
from pylab import *
# plot gaussian

# gamma function
t = 0
N = 15

def ttest(null_dat,test_dat,tcrit=0,sig_lvl=0.05,axis=0,diff=False): # diff represents whether the samples sizes are different (i.e. for max-min)
	try:
		if diff == True:
			if tcrit == 0:
				# calculate degress of freedom and assuming approx equal variance for each lat-lon
				s1, s2 = np.var(null_dat), np.var(test_dat)
				n1, n2 = float(len(null_dat)), float(len(test_dat))
				dof = (s1/n1 + s2/n2)**2/((s1/n1)**2/(n1-1)+(s2/n2)**2/(n2-1))
				print "dof: "+str(dof)
				print "C_n: "+str(1-sig_lvl/2.0)
				exit(0)
			# calculate t values for unequal sampel sizes
			print null_dat.shape
			t = np.zeros(null_dat[0].shape)
			s1, s2 = np.var(null_dat,0), np.var(test_dat,0)
			n1, n2 = float(len(null_dat)), float(len(test_dat))
			tcrit = np.zeros(t.shape) + tcrit
			for lat in range(len(t)):
				for lon in range(len(t[0])):
					std_12 = (s1[lat][lon]/n1 + s2[lat][lon]/n2)**0.5
					if std_12 != 0: 
						t[lat][lon] = (np.mean(test_dat,0)[lat][lon] - np.mean(null_dat,0)[lat][lon])/std_12
						print t[lat][lon]
					print np.mean(t)
					if t[lat][lon] > tcrit[lat][lon] or t[lat][lon] < -tcrit[lat][lon]:	t[lat][lon] = 1
					else: t[lat][lon] = 0
		if diff != True:
			if tcrit == 0:
				print "dof: "+str(len(test_dat))
				print "C_n: "+str(1-sig_lvl/2.0)
				exit(0)
			#calculate t value to find confidence limit for
			t = np.zeros(null_dat[0].shape)
			# print t.shape,null_dat[0]
			tcrit = np.zeros(t.shape) + tcrit
			for lat in range(len(t)):
				for lon in range(len(t[0])):
					if np.std(test_dat,0)[lat][lon] != 0: 
						t[lat][lon] = (np.mean(test_dat,0)[lat][lon] - np.mean(null_dat,0)[lat][lon])/(np.std(test_dat,0)[lat][lon]/((len(test_dat)-1)**0.5))
					if t[lat][lon] > tcrit[lat][lon] or t[lat][lon] < -tcrit[lat][lon]:	t[lat][lon] = 1
					else: t[lat][lon] = 0
		return t

	except ValueError as err:
		print "Value Error: " + str(err)


a = np.array([[[0.02],[-0.06]],[[0.79],[-0.68]]])
b = np.array([[[0.005,0.01],[0.06,0.08]],[[0.79,0.85],[-0.98,-0.41]]])

# ttest(a,b,4.30)

def monte(all_data,solar_data,diff,clim,trials=1000,cutoff=0.95):
	from numpy import zeros
	from random import randint
	# generate trial values for analysis
	for trial in range(trials):
		#generate len(solar_data) random years and initial zero array
		test = zeros(all_data[0].shape)
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
			# reshape for concatenation
			values.shape = (len(values),len(values[0]),1)
		# same method as above for subsequent trials
		elif trial != 0:
			tmp = np.array(test/len(solar_data)-clim)
			tmp.shape = (len(values),len(values[0]),1)
			# concatenate arrays to form final array
			values = np.concatenate((values,tmp),2)
	# reshape difference array for concatenation
	diff.shape = (len(values),len(values[0]),1)
	# return the index within each element of the array that will sort the values
	tmp = np.mean(values,axis=2)
	values = np.concatenate((values,diff),2).argsort().argsort() # this second argsort is essential
	tmp2 = values
	# account for odd behaviour for when both are zero
	for lat in range(len(values)):
		for lon in range(len(values[lat])):
			if values[lat][lon][-1] == trials:# and diff[lat][lon][0] == 0:
				values[lat][lon][-1] = trials/2
	# isolate index that the difference array will need when sorting
	sig = np.delete(values,s_[:-1],2)
	# reshape array to lat/lon style
	sig.shape = (len(values),len(values[0]))
	# transform indices into probabilities
	sig = sig.astype(float)/float(trials)
	# identify significant values in a 1|0 system
	lower = (1-cutoff)/2
	opt = zeros(sig.shape)
	for lat in range(len(values)):
		for lon in range(len(values[lat])):
			if sig[lat][lon] > cutoff+lower: opt[lat][lon] = 1
			if sig[lat][lon] < lower: opt[lat][lon] = 1
	return opt.astype(int)

def sig_test(list_dir='/media/jonathan/KINGSTON/blocking/gen_data/',data_dir='/media/jonathan/KINGSTON/blocking/data/pkl_files/blocking/',monte=True,sttest=False,tcrit=0,list_name='era40_blocking_thpv2.list',high=True,month='thpv2',trials=1000,cutoff=0.8):
	try:
		from open import stdata
		from open import read_list
		from numpy import zeros
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
		diff = np.array(solar_data)-np.array(clim)
		# t-test to find significant lat-lon points at a specific confidence level
		if sttest == True:
			opt = ttest(zeros(diff.shape),diff,tcrit)
			return opt
		# monte carlo bootstrap method for determining a lat/lon array of significances
		if monte == True:
			from random import randint
			# generate trial values for analysis
			for trial in range(trials):
				#generate len(solar_data) random years and initial zero array
				test = zeros(all_data[0].shape)
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
			print values.shape
			fig = plt.figure()
			plt.hist(values[6][18])
			axes = plt.gca()
			# axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
			# axes.plot(x, y, 'r')
			axes.set_xlabel(xlabel)
			axes.set_ylabel(ylabel)
			plt.title(title);
			fig.show()
			print diff[6][18]
			# reshape difference array for concatenation
			diff.shape = (len(values),len(values[0]),1)
			# return the index within each element of the array that will sort the values
			tmp = np.mean(values,axis=2)
			values = np.concatenate((values,diff),2).argsort().argsort() # this second argsort is essential
			tmp2 = values
			# print values
			# account for odd behaviour for when both are zero
			for lat in range(len(values)):
				for lon in range(len(values[lat])):
					if values[lat][lon][-1] == trials:# and diff[lat][lon][0] == 0:
						values[lat][lon][-1] = trials/2
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
			opt = zeros(sig.shape)
			for lat in range(len(values)):
				for lon in range(len(values[lat])):
					if sig[lat][lon] > cutoff+lower: opt[lat][lon] = 1
					if sig[lat][lon] < lower: opt[lat][lon] = 1
			# opt2 = - (sig - (1+lower)).astype(int)
			# #values > upper limit
			# opt2 = opt2 + (sig + (1-cutoff)/2).astype(int)
			# for lat in range(len(values)):
			# 	for lon in range(len(values[lat])):
			# 		if opt1[lat][lon] != opt2[lat][lon]:
			# 			print lat*3.72,lon*3.75,diff[lat][lon],tmp[lat][lon],opt1[lat][lon],opt2[lat][lon],tmp2[lat][lon][-1]
			return opt.astype(int)

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)

sig_test(sttest=True,tcrit=1.74)