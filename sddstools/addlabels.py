import matplotlib.pyplot as _plt
# Add labels to figures
def addlabels(xl,yl,tl):
	fig=_plt.gcf()
	fig.suptitle(tl)
	_plt.xlabel(xl)
	_plt.ylabel(yl)
	showfig(fig)
