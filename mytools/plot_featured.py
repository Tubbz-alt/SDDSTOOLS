#!/usr/bin/env python
import numpy as _np
import matplotlib.pyplot as _plt

def plot_featured(*args,**kwargs):
	"""Wrapper for matplotlib.pyplot.plot()/errorbar().
	Example:  plot_featured(x,y,[arguments to matplotlib.pyplot.plot()/errorbar()],
			[toplabel=],[xlabel=],[ylabel=],
			[legend=],
			[error=]
			)
	"""
	# Strip off options specific to plot_featured
	toplabel = kwargs.pop('toplabel',None)
	xlabel   = kwargs.pop('xlabel',None)
	ylabel   = kwargs.pop('ylabel',None)
	legend   = kwargs.pop('legend',None)
	error    = kwargs.pop('error',None)
	save     = kwargs.pop('save',False)

	# Pass everything else to plot
	if ( error == None ):
		plt.plot(*args,**kwargs)
	else:
		plt.errorbar(*args,**kwargs)

	# Format plot as desired
	mt.addlabel(toplabel,xlabel,ylabel)
	if ( legend != None ):
		plt.legend(legend)
