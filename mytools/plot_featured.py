#!/usr/bin/env python
import numpy as _np
import matplotlib.pyplot as _plt
from addlabel import addlabel as _addlabel
from figure import _figure

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
	figlabel = kwargs.pop('figlabel',None)
	fig      = kwargs.pop('fig',None)

	if not (figlabel == None):
		fig=_figure(figlabel)
	elif fig==None:
		try:
			fig=_plt.gcf()
		except:
			fig=_plt.fig()

	# Pass everything else to plot
	if ( error == None ):
		_plt.plot(*args,**kwargs)
	else:
		_plt.errorbar(*args,**kwargs)

	# Format plot as desired
	_addlabel(toplabel,xlabel,ylabel)
	if ( legend != None ):
		_plt.legend(legend)

	return fig
