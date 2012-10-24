from sdds import sddsdata


def printpage(sddsobj):
	numberOfColumns = len(sddsobj.columnName)
	a=[[] for i in range(numberOfColumns) ]
	print a
	# for i in range(numberOfParameters):
	#         sddsobj.parameterData[i].append(sddsdata.GetParameter(sddsobj.index,i))
	for i in range(numberOfColumns):
		a[i].append(sddsdata.GetColumn(sddsobj.index,i))

	print a
	print a[1][0][0]
