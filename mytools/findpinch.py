import argparse
import numpy as _np
import matplotlib.pyplot as _plt
import mytools as _mt
# import copy
import pdb as _pdb

def findpinch(img,xbounds=None,ybounds=None,step=1,verbose=False):
	# ======================================
	# Translate to clearer variables
	# ======================================
	xstart = xbounds[0]
	xstop  = xbounds[1]
	ystart = ybounds[0]
	ystop  = ybounds[1]

	xrange = slice(xstart,xstop)
	yrange = slice(ystart,ystop)

	img=img[yrange,xrange]
	if verbose:
		fig=_mt.figure('To process')
		_plt.imshow(img)
		_plt.show()
	
	# ======================================
	# Check number of points and
	# initialize arrays
	# ======================================
	num_pts   = (ystop-ystart)/step
	sigs      = _np.zeros(num_pts)
	variance  = _np.zeros(num_pts)
	stddev    = _np.zeros(num_pts)
	varerr    = _np.zeros(num_pts)
	chisq_red = _np.zeros(num_pts)
	
	# ======================================
	# Fit individual slices
	# ======================================
	for i,val in enumerate(_mt.linspacestep(0,ystop-ystart-step,step)):
		# Take a strip of the image
		strip = img[slice(val,val+step),:]
		
		# Sum over the strip to get an average of sorts
		histdata = _np.sum(strip,0)
		xbins = len(histdata)
		x = _np.linspace(1,xbins,xbins)
		if verbose:
			_plt.plot(x,histdata,'.-')
			_plt.show()
			_pdb.set_trace()
		
		# Fit with a Gaussian to find spot size
		# plotbool=True
		plotbool = False
		varbool  = False
		popt,pcov,chisq_red[i] = _mt.gaussfit(
				x,
				histdata,
				sigma_y=_np.ones(xbins),
				plot=plotbool,
				variance_bool=varbool,
				background_bool=True,
				verbose=False)
	
		variance[i] = popt[2]
	
	# ======================================
	# Fit 2nd-deg poly to results
	# ======================================
	yvar=_np.shape(_mt.linspacestep(ystart,ystop,step))[0]-1
	yvar=_mt.linspacestep(1,yvar)
	
	out=_np.polyfit(yvar,variance,2)

	if verbose:
		_plt.plot(yvar,variance,yvar,_np.polyval(out,yvar))
		_plt.show()

	# ======================================
	# Report minimum in steps and pixels
	# ======================================
	fitmin=-out[1]/(2*out[0])
	pxmin = fitmin*step+ystart

	print 'Minimum at {} step, {}px'.format(fitmin,pxmin)
