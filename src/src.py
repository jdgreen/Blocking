#import functions

#determine correct directory to use
try:
	import os
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

import open
import ttest
import plots
import sig_test
import func


# func.diff(king,king_dat,king_gra,sig=True,monte=False,sttest=True,tcrit=1.74,filled=False,high=True,cutoff=0.9)
#print sig_test.sig_test(king,king_dat,monte=False,sttest=True,tcrit=2.12)
#func.diff(king,king_dat)

