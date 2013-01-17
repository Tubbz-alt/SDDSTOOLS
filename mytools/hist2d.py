import numpy as np
import matplotlib.pyplot as plt
from showfig import showfig
from addlabel import addlabel

def hist2d(x, y, bins=10, labels=None, aspect="auto", plot=True, fig=None, range=None):
	"""Creates a 2D histogram of data."""

	h,xe,ye=np.histogram2d(x,y,bins=bins,range=range)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	# fig=plt.figure()
	if plot:
		if ( fig==None ):
			fig=plt.gcf()
		ax=fig.gca()
		ax.clear()
		img=ax.imshow(h.transpose(),extent=extent,interpolation="none",aspect=aspect)
		plt.colorbar(img)
		if ( labels != None ):
			addlabel(labels[0],labels[1],labels[2])

		showfig(fig,aspect)
	return h,extent

