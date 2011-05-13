#!/usr/bin/env python
import argparse
import shlex
from subprocess import call

def runElegant(elefile,cores):
	print("Boxcar enabled.\nRunning " + elefile + " with Pelegant...")
	call(shlex.split("bsub -N -u fc49ca.1284327@push.boxcar.io -a mympi -q beamphysics -n " + str(cores) + " -o run.log Pelegant " + elefile))

if __name__ == '__main__':
	parser=argparse.ArgumentParser(version='%(prog)s v0.1',description='Process command line.')
	parser.add_argument('inputfile',action='store',
			help='Elegant input deck.')
	parser.add_argument('-n','--number', action='store', type=int, default=10,
			help='Number of cores to use.')
	arg=parser.parse_args()
	runElegant(arg.inputfile,arg.number)
