import pickle
from numpy import zeros
import numpy as np

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

def read_list(filelist,directory,numpy=True):
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

def stdata(datalist,directory,monthly='thpv2',daily=False,total=False,numpy=True):
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