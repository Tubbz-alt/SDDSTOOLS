import numpy as np
import matplotlib.pyplot as plt
from showfig import showfig

def hist2d(x,y,bins=10,aspect="auto",plot=True,range=None):
	"""Creates a 2D histogram of data."""

	h,xe,ye=np.histogram2d(x,y,bins=bins,range=range)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	# fig=plt.figure()
	if plot:
		fig=plt.gcf()
		ax=fig.gca()
		ax.clear()
		img=ax.imshow(h.transpose(),extent=extent,interpolation="none",aspect=aspect)
		plt.colorbar(img)
		showfig(fig,aspect)
	return h,extent

