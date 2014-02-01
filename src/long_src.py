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
from pylab import *

################
# testing area #
################



##########################
# generate max-min plots #
##########################

# identify run used
run = 'xfwnl'
dat = king_xfwnl
print 'Run:  '+str(run)

# indicators of difference array type
mnmx = True
mxcl = False
mncl = False

# indicator of significance
sig = True
if sig == True: print 'Sig:  '+str(sig)

# critical t value (to be entered manually)
tcrit = 2.03
sig_lvl = 0.05
cutoff = 0.9

# output file name and othe graphing options
graph = True
stype = 'ttest'
output = '/media/jonathan/KINGSTON/blocking/graphs/test.'
filled = False

	
# open and read list into an array
import open
all_data = open.stdata(king_list+str(run)+'/'+str(run)+'.1860-2010.thpv2_months.list',dat,monthly='thpv2',daily=False,total=False,numpy=True)

# extract the high/low time values

# identify start
start = 1860
jump1 = 1940
jump2 = 1950
jump3 = 2010

from solar import quantile

# check TSI wrt time

def check_TSI(start=1860,end=2100,compress=True,graph=False):
	# open data files 
	from open import open_pkl
	data = open_pkl(king_sol,'TSI.year1860-2100.month01-12.sf.pkl') # this is in months inclusive of BOTH end years
	months = data['sf']
	months.shape = (months.shape[0]/12,12)
	if compress == True:
		# define empty array
		tsi = np.array([])
		i = 1
		# exclude end winters as they do not have fully representative values
		for year in range(start,end):
			tmp = np.array([months[i][0],months[i][1],months[i-1][11]])
			tsi = np.append(tsi,np.mean(tmp))
			i += 1
			pass
		# print 'The TSI distribution runs from '+str(start)+' to '+str(end-1)
	if graph == True:
		from plots import line
		line(range(start,end),tsi,'TSI distribution from '+str(start)+'-'+str(end-1),'years','TSI',king_gra+'long_run/tsi_'+str(start)+'-'+str(end)+'month12-14.png')
	return tsi

# get TSI and identify sections to use
tsi = check_TSI()
first = tsi[:jump1-start]
second = tsi[jump2-start:jump3-start]
third = tsi[jump3-start:]

# return quantile values

# for 1860-1940
quant_max1 = quantile(first,kth=2) 
quant_min1 = quantile(first,kth=1) 
# print quant_max1 + start, quant_min1 + start

# for 1950-2010
quant_max2 = quantile(second,kth=2) 
quant_min2 = quantile(second,kth=1) 
# print quant_max2 + jump2, quant_min2 + jump2

# for 1950-2010
quant_max3 = quantile(third,kth=2) 
quant_min3 = quantile(third,kth=1) 
# print quant_max3 + jump3, quant_min3 + jump3

scmax = all_data[quant_max2]
scmin = all_data[quant_min2]

# get difference arrays

from numpy import zeros

if mnmx == True:
	typ = 'Min-Max'
	diff = np.mean(scmax,0) - np.mean(scmin,0)
	test_dat1,test_dat2 = scmax, scmin

if mxcl == True:
	typ = 'Max-Clim'
	diff = np.mean(scmax,0) - np.mean(all_data,0)
	test_dat1,test_dat2 = np.zeros(scmax.shape), scmax - np.mean(all_data,0)

if mncl == True:
	typ = 'Min-Clim'
	diff = np.mean(scmin,0) - np.mean(all_data,0)
	test_dat1,test_dat2 = np.zeros(scmin.shape), scmin - np.mean(all_data,0)

# print result for clarification
print 'Type: '+typ

# get lat-lon coordinates of these arrays and append to a matrix
from open import open_pkl
opt = []
data_xy = open_pkl(dat,str(run)+'.pj.year-2010.month-02.b.thpv2_003.duration_ge_5_day.pkl')
Lon,Lat = data_xy['lon']['lon'],data_xy['lat']['lat']
Lon = np.append(Lon,360+Lon[0])
X,Y = meshgrid(Lon,Lat)
opt.append(X)
opt.append(Y)

# obtain final value for diff so values overlap
a = zeros((len(diff),1))
diff = np.concatenate((diff,a),axis=-1)
for lat in range(0, len(diff)):
	diff[lat][-1] = diff[lat][0]
opt.append(diff)

if sig == True:	
	try: 
		from sig_test import ttest
		regions = ttest(test_dat1,test_dat2,tcrit=tcrit,sig_lvl=sig_lvl,diff=mnmx)
		extra = regions[:,0]
		extra.shape = (regions[:,0].shape[0],1)
		regions = np.concatenate((regions,extra),1)
	except ValueError as err:	print "Value Error: " + str(err)

if graph == True:

	# generate output filename
	sgtype = 'ttest'
	output = str(output)+'_blk_'+str(typ)+'_'+str(sgtype)+'_'+str(int(100*(1-cutoff)+1))

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
 		output = str(output)+'.sig'
 		# masking the array 
		regions = np.ma.array(regions)
		interior = regions < 0.5
		regions[interior] = np.ma.masked
		s = map.contourf(x,y,regions,1,cmap=cm.gray_r)
		t = ax.set_title(str(run)+'.blk.'+str(stype)+'.'+str(typ)+' Sig: ('+str(int(100*(1.0-cutoff)+1))+'%)')
	fig.savefig(str(output)+'.png')
