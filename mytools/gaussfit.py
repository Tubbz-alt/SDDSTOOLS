import numpy as _np
import scipy.optimize as _spopt
import matplotlib.pyplot as _plt

def _gauss(x,amp,mu,sigma,bg=0):
	return amp*_np.exp(-(x-mu)**2/(2*sigma**2))+bg

def _gaussvar(x,amp,mu,variance,bg=0):
	return amp*_np.exp(-(x-mu)**2/(2*variance))+bg

def gaussfit(x, y, sigma_y=None, plot=True, p0=None, verbose=False, variance_bool=False):
	x       = x.flatten()
	y       = y.flatten()

	# Determine whether to use the variance or std dev form
	# in the gaussian equation
	if variance_bool:
		func = _gaussvar
	else:
		func = _gauss

	# Diagnostics
	# print 'X shape = {}'.format(x.shape)
	# print 'Y shape = {}'.format(y.shape)
	# print 'sigma_y shape = {}'.format(sigma_y.shape)


	# Determine initial guesses if none are input
	if ( p0 == None):
		# print 'hi'
		amp = max(y)
		mu  = sum(x*y)/sum(y)
		rms = _np.sqrt(sum(x**2 * y)/sum(y))
		bg  = 0
		if variance_bool:
			p0 = _np.array((amp,mu,rms**2,bg))
		else:
			p0 = _np.array((amp,mu,rms,bg))

	if verbose:
		print 'Initial guess is: {}'.format(p0)
		print 'RMS is: {}'.format(rms)

	if ( sigma_y != None ):
		popt,pcov = _spopt.curve_fit(func,x,y,sigma=sigma_y,p0=p0)
	else:
		popt,pcov = _spopt.curve_fit(func,x,y,p0=p0)

	if verbose:
		print 'Fit results are: {}'.format(popt)
		print 'Covariance matrix is: {}'.format(pcov)
	if plot:
		xmin = min(x)
		xmax = max(x)
		x_fit = _np.linspace(xmin,xmax,1000)
		y_fit = func(x_fit,popt[0],popt[1],popt[2],popt[3])
		if ( sigma_y != None ):
			sigma_y = sigma_y.flatten()
			_plt.errorbar(x,y,yerr=sigma_y,fmt='o-')
			_plt.plot(x_fit,y_fit)
		else:
			_plt.plot(x,y,'o-',x_fit,y_fit)

	red_chisq = mt.chisquare(y,y_fit,sigma_y,3)

	return popt,pcov,red_chisq
