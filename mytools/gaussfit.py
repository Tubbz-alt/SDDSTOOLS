import numpy as _np
import scipy.optimize as _spopt
import matplotlib.pyplot as _plt
from chisquare import chisquare as _chisquare
from curve_fit_unscaled import curve_fit_unscaled as _curve_fit_unscaled

def _gauss(x,amp,mu,sigma,bg=0):
	# return _np.abs(amp)*_np.exp(-(x-mu)**2/(2*sigma**2))+bg
	return _np.abs(amp)*_np.exp(-(x-mu)**2/(2*sigma**2))

def _gaussvar(x,amp,mu,variance,bg=0):
	return _np.abs(amp)*_np.exp(-(x-mu)**2/(2*variance))+bg

def gaussfit(x, y, sigma_y=None, plot=True, p0=None, verbose=False, variance_bool=False):
	x       = x.flatten()
	y       = y.flatten()

	use_error = ( sigma_y != None )

	# Determine whether to use the variance or std dev form
	# in the gaussian equation
	if variance_bool:
		func = _gaussvar
	else:
		func = _gauss

	# Determine initial guesses if none are input
	if ( p0 == None):
		amp = max(y)
		mu  = sum(x*y)/sum(y)
		rms = _np.sqrt(sum(x**2 * y)/sum(y))
		bg  = 0
		if variance_bool:
			p0 = _np.array((amp,mu,rms**2,bg))
		else:
			p0 = _np.array((amp,mu,rms,bg))
	else:
		if variance_bool:
			rms = _np.sqrt(p0[2])
		else:
			rms = p0[2]


	# Verbose options
	if verbose:
		if variance_bool:
			print 'Using function gaussvar'
		else:
			print 'Using function gauss'
		print 'Initial guess is: {}'.format(p0)
		print 'RMS is: {}'.format(rms)

	popt,pcov,chisq_red = _curve_fit_unscaled(func,x,y,sigma=sigma_y,p0=p0)
	# # Either with error or without
	# if use_error:
	#         if verbose: print 'With error'
	#         popt,pcov = _spopt.curve_fit(func,x,y,sigma=sigma_y,p0=p0)

	#         # Get reduced chi-square
	#         y_expect = func(x,popt[0],popt[1],popt[2],popt[3])
	#         chisq_red = _chisquare(y,y_expect,sigma_y,3,verbose=verbose)

	#         # Correct scaled covariance matrix
	#         pcov = pcov/chisq_red
	# else:
	#         if verbose:
	#                 print 'Without error'
	#                 print 'WARNING: COVARIANCE MATRIX SCALED'
	#         popt,pcov = _spopt.curve_fit(func,x,y,p0=p0)

	popt[2] = _np.abs(popt[2])

	if verbose:
		print 'Fit results are: {}'.format(popt)
		print 'Covariance matrix is: {}'.format(pcov)
	if plot:
		xmin = min(x)
		xmax = max(x)
		x_fit = _np.linspace(xmin,xmax,1000)
		y_fit = func(x_fit,popt[0],popt[1],popt[2],popt[3])
		if use_error:
			sigma_y = sigma_y.flatten()
			_plt.errorbar(x,y,yerr=sigma_y,fmt='o-')
			_plt.plot(x_fit,y_fit)
		else:
			_plt.plot(x,y,'o-',x_fit,y_fit)

	if use_error:
		return popt,pcov,chisq_red
	else:
		return popt,pcov
