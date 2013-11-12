import numpy as _np
from sdds2array import sdds2array as _sdds2array

# Create a histogram from an sdds file.
def sddshist2d(filename,array,bins=10):
	this=sddsload(filename)

	for i,label in enumerate(array):
		if label=='z':
			t=_sdds2array(this,'t')
			dt=t-_np.mean(t)
			temp=dt*299792458
		elif label=='dp':
			p=_sdds2array(this,'p')
			temp=(p-_np.mean(p))/_np.mean(p)
		else:
			temp=_sdds2array(this,label)
		if i==0:
			x=temp
		else:
			y=temp
	
	hist2d(x,y,bins)
	addlabels(array[0],array[1],'')
