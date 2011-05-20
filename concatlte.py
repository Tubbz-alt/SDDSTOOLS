#!/usr/bin/env python
import argparse
import shutil
import os
import sys

def concatlte(inputfile,outputfile,verbose):
# Concatenates into final run.lte
	# Notification that code will overwrite output file
	if os.path.exists(outputfile) & verbose: print("Will overwrite existing file " + outputfile + "...")

	# Concatenates files
	if verbose: print("Concatenating prepend.lte, " + inputfile + ", and append.lte...")
	filelist=['prepend.lte',inputfile,'append.lte']
	fileobj=[]
	# Open files to write from (and make sure
	# they can be opened!)
	for curfile in filelist:
		# temp=open(curfile)
		try:
			fileobj.append(open(curfile))
		except:
			print("File does not exist: " + curfile)
			sys.exit()
	filedest=open(outputfile,'w')
	for curfile in fileobj:
		shutil.copyfileobj(curfile,filedest)
	filedest.close()

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description=
			'Concatenates lattice files into one file to be used in a Pelegant simulation.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('inputfile',
			help='Yuri\'s lattice.')
	parser.add_argument('outputfile',
			help='Output filename for concatenated lattice.')
	arg=parser.parse_args()
	concatlte(arg.inputfile,arg.outputfile,arg.verbose)
