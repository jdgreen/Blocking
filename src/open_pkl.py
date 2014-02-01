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