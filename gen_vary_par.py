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

	header=list(rdr.next())
	header=list(rdr.next())
	print len(header)
	rdrlist=list(rdr)
	
	par=open(outputf + ".tmp",'w')
	wrtr=csv.writer(par,dialect='parout')

	for j in rdrlist:
		# row=[j[0].strip(), header[i].strip(), j[i].strip()]
		row=j
		
		# for k in j:
		#         row= row + [k]

		if verbose:
			print row
		# Write to file to be parsed by plaindata2sdds
		wrtr.writerow(row)
	
	f.close()
	par.close()

	columnStr=''
	for j in range(0,len(header)):
		# print header[j]
		columnStr=columnStr + '-col=' + header[j] + ',double '
	print columnStr
	# Change intermediate file to .par file
	command="plaindata2sdds " + outputf + ".tmp " + outputf + " " + columnStr + "-noRowCount -outputMode=binary \"-separator= \""
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
