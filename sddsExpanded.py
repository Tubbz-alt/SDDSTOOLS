# Extends default sdds python toolkit.
import sdds
import numpy as np
import matplotlib.pyplot as plt

# Converts sdds to an array.
def sdds2array(instance,var):
	return np.array(instance.columnData[instance.columnName.index(var)][0])

# 2-D histogram
def hist2d(x,y,bins=10):
	h,xe,ye=np.histogram2d(x,y,bins=bins)
	extent=[xe[0],xe[-1],ye[-1],ye[0]]
	# fig=plt.figure()
	fig=plt.gcf()
	ax=fig.gca()
	ax.clear()
	ax.imshow(h.transpose(),extent=extent)


	showfig(fig)
	return h,extent

	# fig=plt.figure()
	# ax=fig.add_subplot(111)
	# ax.imshow(h,extent=extent)

	# fig.show()
	# return fig

# Show and configure any figure
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

# Add labels to figures
def addlabels(xl,yl,tl):
	fig=plt.gcf()
	fig.suptitle(tl)
	plt.xlabel(xl)
	plt.ylabel(yl)
	showfig(fig)

# Create a histogram from an sdds file.
def sddshist2d(filename,array,bins=10):
	this=sddsload(filename)

	for i,label in enumerate(array):
		if label=='z':
			t=sdds2array(this,'t')
			dt=t-np.mean(t)
			temp=dt*299792458
		elif label=='dp':
			p=sdds2array(this,'p')
			temp=(p-np.mean(p))/np.mean(p)
		else:
			temp=sdds2array(this,label)
		if i==0:
			x=temp
		else:
			y=temp
	
	hist2d(x,y,bins)
	addlabels(array[0],array[1],'')

# Load an sdds file.
def sddsload(filename):
	this=sdds.SDDS(0)
	this.load(filename)
	return this
