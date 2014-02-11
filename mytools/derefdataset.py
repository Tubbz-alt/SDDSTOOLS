import numpy as _np

def derefdataset(dataset,f):
	# Get the dataset shape, initialize output
	out = _np.empty(dataset.shape[0])

	# Iterate over references, save to out.
	for i,val in enumerate(dataset):
		out[i] = f[val[0]][0,0]

	return out
