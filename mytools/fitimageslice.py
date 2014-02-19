from gaussfit import gaussfit as _gaussfit
import numpy as _np

def fitimageslice(img,res,xslice,yslice):
		# Take a strip of the image
		# strip = img[slice(475,480),yrange]
		strip = img[xslice,yslice]
		# fig=mt.figure('Strip')
		# plt.imshow(strip)
		
		# Sum over the strip to get an average of sorts
		histdata = sum(strip)
		xbins = len(histdata)
		x = _np.linspace(1,xbins,xbins)*res
		# plt.plot(x,histdata)
		
		# Fit with a Gaussian to find spot size
		# fig=mt.figure('Gaussian Fit')
		# plotbool=True
		plotbool = False
		# varbool  = False
		varbool  = True
		# popt,pcov,chisq_red = _gaussfit(x,histdata,sigma_y=_np.ones(xbins),plot=plotbool,variance_bool=varbool,verbose=False,p0=[16000,3500,500])
		return _gaussfit(x,histdata,sigma_y=_np.ones(xbins),
				plot=plotbool,
				variance_bool=varbool,
				verbose=False,
				p0=[16000,0.003,1e-6])
