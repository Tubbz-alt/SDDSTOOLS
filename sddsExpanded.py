import sdds
import numpy as np
import matplotlib.pyplot as plt

def sdds2array(instance,var):
	return np.array(instance.columnData[instance.columnName.index(var)][0])

def hist2d(x,y,bins=10):
	h,xe,ye=np.histogram2d(x,y,bins=bins)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	fig=plt.gcf()
	ax=fig.gca()
	ax.imshow(h.transpose(),extent=extent)


	showfig(fig)
	return h,extent

	# fig=plt.figure()
	# ax=fig.add_subplot(111)
	# ax.imshow(h,extent=extent)

	# fig.show()
	# return fig

def showfig(fig):
	ax=fig.gca()
	# Swap y axis if needed
	alim=list(ax.axis())
	if alim[3]<alim[2]:
		temp=alim[2]
		alim[2]=alim[3]
		alim[3]=temp
		ax.axis(alim)
	ax.set_aspect('auto')
	fig.show()

def addlabels(xl,yl,tl):
	pass
