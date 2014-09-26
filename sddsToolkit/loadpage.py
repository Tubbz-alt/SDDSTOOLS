#!/usr/bin/env python
import sdds
sddsdata=sdds.sddsdata
import sys, time
# from collections import deque
import numpy as np
import os

def loadpage(filename,pagenum=1):
	'''Loads a single page and returns an SDDS class.
	
	Arguments:
	filename -- the file to load
	pagenum  -- the page(s) to load: int, list, or ndarray format (default: 1)
	'''
	sddsobj=sdds.SDDS(0)

	# Test for page existence
	if not ( os.path.exists(filename) ):
		raise IOError('File \'{}\' not found!'.format(filename))

	# Set up so that multiple pages can be loaded.
	if type(pagenum) == int:
		# Turn into a list.
		pagenum=[pagenum]
	elif type(pagenum) == list:
		pagenum.sort()
	elif type(pagenum) == np.ndarray:
		pagenum=pagenum.astype(int).tolist()
	else:
		print "Not a list or an int."
		return

	try:
		#open SDDS file
		if sddsdata.InitializeInput(sddsobj.index, filename) != 1:
		     time.sleep(2)
		     print "test"
		     if sddsdata.InitializeInput(sddsobj.index, filename) != 1:
		          sddsdata.PrintErrors(sddsobj.SDDS_EXIT_PrintErrors)
		
		#get data storage mode (SDDS_ASCII or SDDS_BINARY)
		sddsobj.mode = sddsdata.GetMode(sddsobj.index)
		
		#get description text and contents
		sddsobj.description = sddsdata.GetDescription(sddsobj.index)
		
		#get parameter names
		sddsobj.parameterName = sddsdata.GetParameterNames(sddsobj.index)
		numberOfParameters = len(sddsobj.parameterName)
		
		#get column names
		sddsobj.columnName = sddsdata.GetColumnNames(sddsobj.index)
		numberOfColumns = len(sddsobj.columnName)
		
		#get parameter definitions
		sddsobj.parameterDefinition = range(numberOfParameters)
		for i in range(numberOfParameters):
			sddsobj.parameterDefinition[i] = sddsdata.GetParameterDefinition(sddsobj.index, sddsobj.parameterName[i])
		
		#get column definitions
		sddsobj.columnDefinition = range(numberOfColumns)
		for i in range(numberOfColumns):
			sddsobj.columnDefinition[i] = sddsdata.GetColumnDefinition(sddsobj.index, sddsobj.columnName[i])
		
		#initialize parameter and column data
		sddsobj.parameterData = range(numberOfParameters)
		sddsobj.columnData = range(numberOfColumns)
		for i in range(numberOfParameters):
			sddsobj.parameterData[i] = []
		for i in range(numberOfColumns):
			sddsobj.columnData[i] = []

		# for i in range(pagenum-1):
		page = 0
		minpage=min(pagenum)
		# print minpage
		maxpage=max(pagenum)
		# Skip over pages before minpage
		while (page < minpage-1):
			page=sddsdata.ReadPageSparse(sddsobj.index,99999999,0)

			if page == 0:
				sddsdata.PrintErrors(sddsobj.SDDS_EXIT_PrintErrors)
			elif page == -1:
				break

		# Keep grabbing pages before maxpage
		# while (page < maxpage-1) and (page > 0):
		for i in range(minpage,maxpage+1):
			toread = pagenum.count(page+1) > 0
			# If the next page is in the list of pages to read, read it.
			if toread:
				page = sddsdata.ReadPage(sddsobj.index)
			else:
				page = sddsdata.ReadPageSparse(sddsobj.index,99999999,0)

			# Check for errors
			if page == 0:
				sddsdata.PrintErrors(sddsobj.SDDS_EXIT_PrintErrors)
			elif page == -1:
				break
			if toread:
				for i in range(numberOfParameters):
					sddsobj.parameterData[i].append(sddsdata.GetParameter(sddsobj.index,i))
				for i in range(numberOfColumns):
					sddsobj.columnData[i].append(sddsdata.GetColumn(sddsobj.index,i))
		
		#close SDDS file
		if sddsdata.Terminate(sddsobj.index) != 1:
			sddsdata.PrintErrors(sddsobj.SDDS_EXIT_PrintErrors)

	except:
		sddsdata.PrintErrors(sddsobj.SDDS_VERBOSE_PrintErrors)
		raise

	return sddsobj
