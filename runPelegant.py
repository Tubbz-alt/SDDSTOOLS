#!/usr/bin/env python
import argparse
import shutil
from subprocess import call
import shlex
import os
import concatlte
import pelnotify

def runPelegant(inputfile, number, verbose):
	
	# Deletes files
	files=['run.lte','run.log','momentumscan.out']
	for thisfile in files:
		try:
			os.remove(thisfile)
		except:
			print("Error removing " + thisfile + ".  (Probably doesn\'t exist.)")
	
	# Informs about the number of cores running
	print("Running on " + str(number) + " cores...")
	
	concatlte.concat(inputfile, 'run.lte', verbose)
	
	pelnotify.runElegant('momentumscan.ele', number)

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description='Process command line.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')

	# Options
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('-n','--number', action='store', type=int, default=10, help='Number of cores to use.')

	# Arguments
	parser.add_argument('deck', action='store', help='Elegant input deck.')
	
	arg=parser.parse_args()

	runPelegant(arg.deck, arg.number, verbose)
