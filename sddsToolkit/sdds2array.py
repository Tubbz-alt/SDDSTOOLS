import numpy as np

def sdds2array(instance,var):
	'''Extracts imported SDDS data to a numpy vector.'''

	if var == 'z':
		ind=instance.columnName.index('t')
	elif var == 'd':
		ind=instance.columnName.index('p')
	else:
		ind=instance.columnName.index(var)

	out = np.array(instance.columnData[ind])

	if var == 'z':
		out = 299792458*(out-np.mean(out))
	elif var == 'd':
		pmean = np.mean(out)
		out = (out-pmean)/pmean

	if len(out) == 1:
		return out[0]
	else:
		return out
