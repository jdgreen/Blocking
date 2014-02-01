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

def ttest():
	pass