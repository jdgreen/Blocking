#get dictionary files
from pylab import *
import matplotlib.pyplot as plt

def line(x,y,title,xlabel,ylabel,output):
	fig = plt.figure()
	plt.plot(x, y, 'r')
	axes = plt.gca()
	# axes = fig.add_axes([0.1, 0.1, 0.8, 0.8]) # left, bottom, width, height (range 0 to 1)
	# axes.plot(x, y, 'r')
	axes.set_xlabel(xlabel)
	axes.set_ylabel(ylabel)
	plt.title(title);
	fig.show()
	fig.savefig(output)

def test(output=''):
	alpha = 0.7
	phi_ext = 2 * pi * 0.5

	def flux_qubit_potential(phi_m, phi_p):
		return 2 + alpha - 2 * cos(phi_p)*cos(phi_m) - alpha * cos(phi_ext - 2*phi_p)

	phi_m = linspace(0, 2*pi, 100)
	phi_p = linspace(0, 2*pi, 100)
	X,Y = meshgrid(phi_p, phi_m)
	Z = flux_qubit_potential(X, Y).T

	fig, ax = plt.subplots()

	p = ax.pcolor(X/(2*pi), Y/(2*pi), Z, cmap=cm.RdBu,alpha=0.2)# vmin=abs(Z).min(), vmax=abs(Z).max(),alpha=0.2)
	cb = fig.colorbar(p, ax=ax)
	fig.savefig(str(output))

def contour_2d():
	pass

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

def contour(output,high=True,blk=True,type='thpv2',col=False):
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
