import numpy as _np
import matplotlib.pyplot as _plt

def hist2d(x,y,bins=10):
	h,xe,ye=_np.histogram2d(x,y,bins=bins)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	# fig=_plt.figure()
	fig=_plt.gcf()
	ax=fig.gca()
	ax.clear()
	ax.imshow(h.transpose(),extent=extent)


	showfig(fig)
	return h,extent
