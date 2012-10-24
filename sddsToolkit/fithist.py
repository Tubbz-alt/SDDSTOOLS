import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

def fithist(res,
		fitfunc=None,
		p0=None
		):
	"""Finds a fit given histogram data."""

	# Define fitfunc if not specified
	if fitfunc == None:
		fitfunc=lambda p, x: p[0]*np.exp(-np.square(x-p[2])/(2*np.square(p[1])))
	errfunc = lambda p, x, y: fitfunc(p,x) - y

	delta=res[1][1]-res[1][0]
	coord=res[1][0:bins]+delta
	counts=res[0]
	
	p0 = [max(counts), np.std(x), np.mean(x)]
	p1, success = spopt.leastsq(errfunc,p0[:],args=(coord,counts))
