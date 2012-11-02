import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt

def fithist(bin_edges,counts,
		fitfunc=None,
		p0=None
		):
	"""Finds a fit given histogram data."""

	# Separation between hist points
	delta=bin_edges[1]-bin_edges[0]
	# Find coordinates - bin_edges returns edges, want center
	coord=bin_edges[0:len(counts)]+delta

	# If there's no fitfunc, assume gaussian distribution
	if fitfunc == None:
		# If there's no guess, come up with one
		if p0 == None:
			# Find average as if all counts are at the center of their bin.
			mean = sum(coord*counts)/sum(counts)
			# Find std dev as if all counts are at the center of their bin.
			std = np.sqrt(sum( counts*((coord-mean)**2) )/sum(counts))
			# print std
			p0 = [max(counts), std, mean]
			print p0
		fitfunc=lambda p, x: p[0]*np.exp(-np.square(x-p[2])/(2*np.square(p[1])))
	errfunc = lambda p, x, y: fitfunc(p,x) - y
	
	p1, success = spopt.leastsq(errfunc,p0[:],args=(coord,counts))

	return p1,success

