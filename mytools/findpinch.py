import argparse
import numpy as _np
import matplotlib.pyplot as _plt
import mytools as _mt
# import copy

def findpinch(img,xbounds=None,ybounds=None,step=1):
	# Translate to clearer variables
	xstart = xbounds[0]
	xstop  = xbounds[1]
	ystart = ybounds[0]
	ystop  = ybounds[1]

	xrange = slice(xstart,xstop)
	yrange = slice(ystart,ystop)

	fig=_mt.figure('To process')
	# a=img
	_plt.imshow(img[xrange,yrange])
	
	# Check number of points and initialize arrays
	num_pts=(xstop-xstart)/step
	sigs=_np.zeros(num_pts)
	# num_pts = len(sum_x)
	variance  = _np.zeros(num_pts)
	stddev    = _np.zeros(num_pts)
	varerr    = _np.zeros(num_pts)
	# print varerr.shape
	chisq_red = _np.zeros(num_pts)
	
	# Fit individual slices
	for i,val in enumerate(_mt.linspacestep(xstart,xstop-step,step)):
		print i
		# Take a strip of the image
		# strip = img[slice(475,480),yrange]
		strip = img[slice(val,val+step),yrange]
		# fig=_mt.figure('Strip')
		# _plt.imshow(strip)
		
		# Sum over the strip to get an average of sorts
		histdata = sum(strip)
		xbins = len(histdata)
		x = _np.linspace(1,xbins,xbins)
		# _plt.plot(x,histdata)
		
		# Fit with a Gaussian to find spot size
		# fig=_mt.figure('Gaussian Fit')
		# plotbool=True
		plotbool = False
		varbool  = False
		# popt,pcov,chisq_red = _mt.gaussfit(x,histdata,sigma_y=_np.ones(xbins),plot=plotbool,variance_bool=varbool,verbose=False,p0=[16000,3500,500,0])
		popt,pcov,chisq_red = _mt.gaussfit(x,histdata,sigma_y=_np.ones(xbins),plot=plotbool,variance_bool=varbool,verbose=False)
	
		variance[i] = popt[2]
		# varerr[i]   = pcov[2,2]
		# stddev[i]   = _np.sqrt(pcov[2,2])
	
	_mt.figure('Varplot')
	# _plt.plot(variance)
	
	xvar=_np.shape(_mt.linspacestep(xstart,xstop,step))[0]-1
	xvar=_mt.linspacestep(1,xvar)
	
	out=_np.polyfit(xvar,variance,2)
	
	_plt.plot(xvar,variance,'.-',xvar,_np.polyval(out,xvar))

	fitmin=-out[1]/(2*out[0])
	pxmin = fitmin*step+xstart

	print 'Minimum at {} step, {}px'.format(fitmin,pxmin)
