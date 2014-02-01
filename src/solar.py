import numpy as np

def quantile(arr,kth=2,type=3):
	#calculate the quantile of a given data set
	try:
		#order the array
		array = sorted(arr)
		lngth = len(arr)
		factor = float(kth)*float(lngth)/float(type)
		#calculate quartile value
		quant = array[int(factor)-1]
		# return array[int(factor)-1]
		#return values of array above or below
		opt = np.array([])
		for index in range(len(arr)):
			if kth == 2: 
				if np.array(arr)[index] > quant: opt = np.append(opt,int(index))
			if kth == 1: 
				if np.array(arr)[index] < quant: opt = np.append(opt,int(index))
		return opt.astype(int)
	except ValueError as err:
		print "Value Error: " + str(err)

def blocking(input,out_dir,start=1958,end=2002,q_type=3,s_type='TSI',high=True,opt=False):
	#produce a list of files of high/low blocking
	#example: source.blocking('/home/loki/mad/green/data/pkl_files/solar_cycle/','OSF.year1675-2010.sf.pkl','../data/')
	try:
		#get options sorted
		if high == True:
			quant,high = 2,'high'
		if high == False:
			quant,high = 1,'low'
		years = []
		count = []

		#options for TSI/OSI
		if s_type == 'TSI':
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
		return years

	except ValueError as err:
		print "Value Error: " + str(err)

def file_blocking(s_dir,s_name,out_dir,start=1958,end=2002,q_type=3,s_type='OSF',high=True,opt=False):
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

def sol_ext(dat_dir,dat_name='_OSF.year1958-2002.sf.pkl',l_name='era40_blocking_thpv2.list',high='high',q_type='OSI',count=3):
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

def years(extra=False):
	d_yrs = {	
			'SCmax' : [1957,1958,1959,1960,1978,1980,1981,1982,1988,1989,1990,1991,1992,1999,2000],
			'SCmin' : [1962,1963,1964,1965,1966,1970,1971,1975,1976,1985,1986,1994,1995,1996,1997]
			}
	if extra == True:
		# add extra years based on what I can make out for the post-2000 years on W10 Fig 1
		d_yrs['SCmax'] += [2002]
		d_yrs['SCmin'] += [2004,2005,2006,2007] 
	return d_yrs
