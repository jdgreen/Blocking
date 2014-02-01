import numpy as np
from pylab import *
# plot gaussian

# gamma function
t = 0
N = 15

def ttest(null_dat,alt_dat,tcrit=0,sig_lvl=0.05,axis=0):
	try:
		if tcrit == 0:
			print "dof: "+str(len(alt_dat))
			print "C_n: "+str(1-sig_lvl/2.0)
			exit(0)

		#calculate t value to find confidence limit for
		t = np.zeros(null_dat[0].shape)
		#(np.mean(alt_dat,0) - np.mean(null_dat,0))/(np.std(alt_dat,0)/((len(alt_dat)-1)**0.5))
		tcrit = np.zeros(t.shape) + tcrit
		for lat in range(len(t)):
			for lon in range(len(t[0])):
				if np.std(alt_dat,0)[lat][lon] != 0: 
					t[lat][lon] = (np.mean(alt_dat,0)[lat][lon] - np.mean(null_dat,0)[lat][lon])/(np.std(alt_dat,0)[lat][lon]/((len(alt_dat)-1)**0.5))
					#print t[lat][lon]
				if t[lat][lon] > tcrit[lat][lon] or t[lat][lon] < -tcrit[lat][lon]:	t[lat][lon] = 1
				else: t[lat][lon] = 0
		return t

	except ValueError as err:
		print "Value Error: " + str(err)

a = np.array([[[0.02],[-0.06]],[[0.79],[-0.68]]])
b = np.array([[[0.005,0.01],[0.06,0.08]],[[0.79,0.85],[-0.98,-0.41]]])

# ttest(a,b,4.30)

def sig_test(list_dir='',data_dir='',monte=True,sttest=False,tcrit=0,list_name='era40_blocking_thpv2.list',high=True,month='thpv2',trials=1000,cutoff=0.95):
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
		diff = np.array(b_hls)-np.array(clim)
		# t-test to find significant lat-lon points at a specific confidence level
		if sttest == True:
			opt1 = ttest(all_data,solar_data,tcrit)
			#return opt
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
			tmp2 = sig
			sig = sig.astype(float)/float(trials)

			# # alternate method - I consider this to be incorrect but did produce okay graphs
			# sig = (values == trials).nonzero()[-1] # sig = sig.astype(float)/float(trials)		#generate an array of 1s and 0s depending if in range of two tailed significance #values <lower limit
			lower = (1-cutoff)/2
			print lower,cutoff,sig.shape
			opt = zeros(sig.shape)
			for lat in range(len(values)):
				for lon in range(len(values[lat])):
					if sig[lat][lon] > cutoff+lower: opt[lat][lon] = 1
					if sig[lat][lon] < lower: opt[lat][lon] = 1
			opt2 = -(sig - (1+lower)).astype(int)
			#values > upper limit
			print int(0-(1+0.05))
			opt2 = opt2 + (sig + (1-cutoff)/2).astype(int)
			for lat in range(len(values)):
				for lon in range(len(values[lat])):
					if opt1[lat][lon] == 1 and opt[lat][lon] == 0:
						print lat*3.72,lon*3.75,diff[lat][lon],tmp[lat][lon],opt1[lat][lon],opt[lat][lon],sig[lat][lon],cutoff+lower,lower
			return opt

	except IOError as err:
		print "File error: " + str(err)

	except ValueError as err:
		print "Value Error: " + str(err)
