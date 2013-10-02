import numpy as _np
import scipy.optimize as _spopt
import matplotlib.pyplot as _plt

def gaussfit(x, y, sigma_y=None, plot = True):

	def _gauss(x,amp,mu,sigma):
		return amp*_np.exp(-(x-mu)**2/(2*sigma**2))

	if ( sigma_y != None ):
		popt,pcov = _spopt.curve_fit(_gauss,x,y,sigma=sigma_y)
	else:
		popt,pcov = _spopt.curve_fit(_gauss,x,y)

	if plot:
		xmin = min(x)
		xmax = max(x)
		x_fit = _np.linspace(xmin,xmax,1000)
		y_fit = _gauss(x_fit,popt[0],popt[1],popt[2])
		_plt.plot(x,y,'o-',x_fit,y_fit)

	return popt,pcov
