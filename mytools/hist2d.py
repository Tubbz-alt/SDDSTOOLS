import numpy as _np
import matplotlib.pyplot as _plt
from showfig import showfig as _showfig
from addlabel import addlabel as _addlabel
from figure import figure as _figure

def hist2d(x, y, bins=10, labels=None, aspect="auto", plot=True, fig=None, range=None):
	"""Creates a 2D histogram of data."""

	h,xe,ye=_np.histogram2d(x,y,bins=bins,range=range)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	# fig=plt.figure()
	if plot:
		if ( fig==None ):
			fig=_figure('hist2d')
		ax=fig.gca()
		ax.clear()
		img=ax.imshow(h.transpose(),extent=extent,interpolation='none',aspect=aspect)
		_plt.colorbar(img)
		if ( labels != None ):
			_addlabel(labels[0],labels[1],labels[2])

		_showfig(fig,aspect)
	return h,extent

