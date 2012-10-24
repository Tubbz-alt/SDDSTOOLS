import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

def fitbunch(x,
		bins=100,
		plot_bool=False,
		fitfunc = None,
		p0 = None,
		):
	"""Bin scatter data and fit with a function (default: gaussian).

	Keyword arguments:
	bins -- the number of bins to use when histogramming (default 100)
	plot_bool -- generate a plot of the fit if true (default False)
	fitfunc -- a lambda function used for fitting.  (default )

	fitfunc:
		fitfunc=lambda p, x: p[0]*np.exp(-np.square(x-p[2])/(2*np.square(p[1])))
	"""

	# Bin the data
	res=np.histogram(x,bins)
	# Separation between hist points
	delta=res[1][1]-res[1][0]
	# Find coordinates - res returns edges, want center
	coord=res[1][0:bins]+delta
	# Readability - counts in each bin
	counts=res[0]

	# If there's no fitfunc, assume gaussian distribution
	if fitfunc == None:
		# If there's no guess, come up with one
		if p0 == None:
			p0 = [max(counts), np.std(x), np.mean(x)]
		fitfunc=lambda p, x: p[0]*np.exp(-np.square(x-p[2])/(2*np.square(p[1])))
	elif fitfunc != None and p0 == None:
		raise ArgumentError('p0','Cannot fit a custom function without a custom guess.')
	errfunc = lambda p, x, y: fitfunc(p,x) - y

	p1, success = spopt.leastsq(errfunc,p0[:],args=(coord,counts))

	if plot_bool:
		plt.close()
		xx = np.linspace(coord.min(),coord.max(),500)
		plt.figure(1)
		plt.plot(coord,counts,'ro',xx,fitfunc(p1,xx),'b-')
		plt.figure(2)
		plt.plot(xx,fitfunc(p1,xx),'b-')

	# Returns sig, mean
	# return p1[1],p1[2]
	return p1,p1[1],p1[2]
