from gaussfit import gaussfit as _gaussfit
import numpy as _np
import pdb as _pdb
import mytools as _mt
import matplotlib.pyplot as _plt
import ButterflyEmittancePython as bt

def fitimageslice(img,res_x,res_y,xslice,yslice,avg_e_func=None,h5file=None):
	# ======================================
	# Extract start and end values
	# (NOT necessarily indices!)
	# ======================================
	x_start = xslice[0]
	x_end   = xslice[1]
	y_start = yslice[0]
	y_end   = yslice[1]

	# ======================================
	# Round to pixel edges.  Pixel edges in
	# px units are at 0.5, 1.5, 2.5, etc.
	# ======================================
	y_low = _np.round(y_start-0.5) + 0.5
	y_high = _np.round(y_end-0.5) + 0.5
	# print '======================'
	# print y_start,y_end,y_end-y_start
	# print y_low,y_high

	# ======================================
	# Take a strip between edges
	# ======================================
	y_px = _mt.linspacestep(1,img.shape[0])
	y_bool = _np.logical_and(y_low<y_px,y_px<y_high)
	strip = img[y_bool,x_start:x_end]

	# ======================================
	# Sum over the strip to get an average 
	# ======================================
	histdata = _np.sum(strip,0)
	xbins = len(histdata)
	x = _np.linspace(1,xbins,xbins)*res_x
	# plt.plot(x,histdata)
	
	# ======================================
	# Fit with a Gaussian to find spot size
	# ======================================
	# plotbool=True
	plotbool = False
	# varbool  = False
	varbool  = True
	gaussout=_gaussfit(x,histdata,sigma_y=_np.ones(xbins),
			plot=plotbool,
			variance_bool=varbool,
			verbose=False,
			background_bool=True,
			p0=[16000,0.003,1e-6,0])

	if avg_e_func != None:
		# ======================================
		# Get average energy of strip
		# ======================================
		# Sum to get relative counts of pixels
		relcounts=_np.sum(strip,1) / _np.float(_np.sum(strip))
		# Integrate each pixel strip
		Eavg=0
		for i,val in enumerate(_mt.linspacestep(y_low,y_high-1)):
			Eavg=Eavg + avg_e_func(val,val+1,h5file,res_y)*relcounts[i]
		return Eavg,gaussout
	else:
		return gaussout
