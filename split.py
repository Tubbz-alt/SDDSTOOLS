#!/usr/bin/env python
import os
import argparse
import shutil
# from shlex import split
import shlex
import glob
from subprocess import call

def splitsdds(inputfile):
	try:
		os.mkdir(inputfile + ".split")
	except:
		print("Overwriting previous...")
		fls=glob.glob(inputfile + ".split/*")
		for cur in fls:
			os.remove(cur)
	call(shlex.split("sddssplit " + inputfile + " -rootname=./" + inputfile + ".split/ -extension=out"))

if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	# parser=argparse.ArgumentParser(version='%(prog)s v0.1',description='Process command line.')
	parser.add_argument('inputfile',action='store',
			help='Elegant input deck.')
	arg=parser.parse_args()

	splitsdds(arg.inputfile)
