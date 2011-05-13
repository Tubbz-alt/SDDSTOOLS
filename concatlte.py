#!/usr/bin/env python
import argparse
import shutil

def concat(inputfile):
# Concatenates into final run.lte
	filelist=['prepend.lte',inputfile,'append.lte']
	filedest=open('run.lte','w')
	for curfile in filelist:
		shutil.copyfileobj(open(curfile),filedest)
	filedest.close()

if __name__ == '__main__':
	parser=argparse.ArgumentParser(version='%(prog)s v0.1',description='Process command line.')
	parser.add_argument('inputfile',action='store',
			help='Elegant input deck.')
	arg=parser.parse_args()
	concat(arg.inputfile)
