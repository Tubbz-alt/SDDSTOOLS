#!/usr/bin/env python
import argparse
import shutil
from subprocess import call
import shlex
import os
import concatlte
import pelnotify

# Parses command line arguments.
parser=argparse.ArgumentParser(version='%(prog)s v0.1',description='Process command line.')

parser.add_argument('-n','--number', action='store', type=int, default=10,
		help='Number of cores to use.')
parser.add_argument('inputfile',action='store',
		help='Elegant input deck.')
arg=parser.parse_args()


# Deletes files
files=['run.lte','run.log','momentumscan.out']
for thisfile in files:
	try:
		os.remove(thisfile)
	except:
		print("Error removing " + thisfile + ".  (Probably doesn\'t exist.)")

# Informs about the number of cores running
print("Running on " + str(arg.number) + " cores...")

concatlte.concat(arg.inputfile)

# Submits job
# call(shlex.split("bsub -N -u fc49ca.1284327@push.boxcar.io -a mympi -q beamphysics -n " + str(arg.number) + " -o run.log Pelegant momentumscan.ele"))

pelnotify.runElegant('momentumscan.ele',arg.number)
