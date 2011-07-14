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
	rdrlist=list(rdr)
	len(rdrlist)
	
	par=open(outputf + ".tmp",'w')
	wrtr=csv.writer(par,dialect='parout')

	print len(header)
	print rdrlist
	for i in range(1,len(header)+1):
		print i
		for j in rdrlist:
			print j[i].strip()
			print "hey"
			row=[j[0].strip(), header[i-1].strip(), j[i].strip()]
			print row
			# print header[i]
			# print i
			wrtr.writerow(row)
	
	f.close()
	par.close()
	command="plaindata2sdds " + outputf + ".tmp " + outputf + " -col=ElementName,string -col=ElementParameter,string -col=ParameterValue,double -noRowCount -outputMode=binary \"-separator= \""
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
