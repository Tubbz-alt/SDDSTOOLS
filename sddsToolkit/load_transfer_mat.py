import numpy as np
from loadpage import loadpage
from sdds2array import sdds2array

def load_transfer_mat(filename):
	'''Loads transfer matrices from a file.
	
	Arguments:
	filename -- filename to load
	'''

	page = loadpage(filename)
	
	R11 = sdds2array(page,'R11')
	R = np.zeros([6,6,R11.size])
	for i in np.linspace(1,6,6):
			for j in np.linspace(1,6,6):
					R[i-1,j-1,:]=sdds2array(page,'R{:.0f}{:.0f}'.format(i,j))

	# In the future: Fails gracefully if T-matrices aren't present
	# try:
	#     for i in np.linspace(1,6,6):
	#             for j in np.linspace(1,6,6):
	#                     R[i-1,j-1,:]=sdds2array(page,'R{:.0f}{:.0f}'.format(i,j))

	return R
