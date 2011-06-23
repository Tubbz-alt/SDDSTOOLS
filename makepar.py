#!/usr/bin/env python
import csv
import argparse
import shlex
from subprocess import call

def makepar(inputf,outputf,verbose):
	csv.register_dialect('par',delimiter=',',skipinitialspace=True)
	csv.register_dialect('parout',delimiter=' ',skipinitialspace=True)
	
	f=open(inputf)
	rdr=csv.reader(f,dialect='par')
	header=list(rdr.next())
	varfmt=list(rdr.next())
	print header
	rdrlist=list(rdr)
	print "rdrlist:"
	print rdrlist
	print len(header)-1
	
	par=open(outputf + ".tmp",'w')
	wrtr=csv.writer(par,dialect='parout')

	# print len(header)
	for i in range(2,len(header)-1):
		for j in rdrlist:
			for k in range(0,len(j)):
				j[k]=j[k].strip()
			if verbose:
				print j
			wrtr.writerow(j)
	
	f.close()
	par.close()

	varstr=""
	for i in range(0,len(header)):
		varstr=varstr + " -col=" + header[i].strip() + "," + varfmt[i].strip()
	command="plaindata2sdds " + outputf + ".tmp " + outputf + " -col=ElementName,string -col=ElementOccurrence,double -col=ElementParameter,string -col=ParameterValue,double -noRowCount -outputMode=binary \"-separator= \""
	if verbose:
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
