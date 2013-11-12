import numpy as _np

def sdds2array(instance,var):
	return _np.array(instance.columnData[instance.columnName.index(var)][0])
