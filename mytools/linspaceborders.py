from linspacestep import linspacestep as _linspacestep

def linspaceborders(arr):
	dela = arr[1]-arr[0]
	start = arr[0]-dela/2
	end = arr[-1]+dela/2
	return _linspacestep(start,end,dela)
