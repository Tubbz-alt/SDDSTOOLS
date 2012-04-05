#!/usr/bin/env python
import csv
import argparse
import shlex
from subprocess import call

def makepar(inputf,outputf,verbose):
	# Specify delimiters for input, intermediate files.
	csv.register_dialect('par',delimiter=',',skipinitialspace=True)
	csv.register_dialect('parout',delimiter=' ',skipinitialspace=True)
	
	# Open for reading with unidentified EOL character
	f=open(inputf,'rU')
	rdr=csv.reader(f,dialect='par')

	# Extract header
	header=list(rdr.next())
	rdrlist=list(rdr)
	
	par=open(outputf + ".tmp",'w')
	wrtr=csv.writer(par,dialect='parout')

	# Find the index for "Occurence" if it exists
	try:
		occ=header.index("Occurence")
	except ValueError:
		occ=0
	
	# Inform if there is occurence data.
	if verbose:
		if occ==0:
			print "No occurence data."
		else:
			print "Occurence at index", occ
		print header

	for j in rdrlist:
		for i in range(1,len(header)):
			# Prevents treating occurence as a parameter.
			if i==occ:
				continue

			# If occurence exists, use it.
			if occ>0:
				row=[j[0].strip(), j[occ], header[i].strip(), j[i].strip()]
			else:
				row=[j[0].strip(), header[i].strip(), j[i].strip()]

			if verbose:
				print row

			# Write to file to be parsed by plaindata2sdds
			wrtr.writerow(row)
	
	f.close()
	par.close()

	# Modify command to include occurrence data.
	if occ>0:
		occstr="-col=ElementOccurence,long "
	else:
		occstr=""

	# Change intermediate file to .par file
	command="plaindata2sdds " + outputf + ".tmp " + outputf + " -col=ElementName,string " + occstr +  "-col=ElementParameter,string -col=ParameterValueString,string -noRowCount -outputMode=binary \"-separator= \""
	if verbose:
		print "Command is:"
		print command
	call(shlex.split(command))



if __name__ == '__main__':
	parser=argparse.ArgumentParser(description=
			'Parses a file into a .par file for load_parameters.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('inputfile',
			help='Input CSV file.')
	parser.add_argument('outputfile',
			help='Output .par file.')
	arg=parser.parse_args()

	makepar(arg.inputfile,arg.outputfile,arg.verbose)
