#!/usr/bin/env python
import argparse
import shlex
from subprocess import *
import textwrap
import glob

def split(verbose,infile,outfile):
	# Break single page into pages with 1k entries max
	# Pipe "file" into stdout
	breakCom  = 'sddsbreak ' + infile + ' -rowlimit=1000 -pipe=output'
	breakArgs = shlex.split(breakCom)
	breakSub  = Popen(breakArgs,stdout=PIPE)

	# Write "file" from stdin to files,
	# 1 page/file.  Format: tempXXX.sdds
	splitCom  = 'sddssplit -pipe=input -rootname=temp'
	splitArgs = shlex.split(splitCom)
	splitSub  = Popen(splitArgs,stdin=breakSub.stdout)

	# Close stdout from input file
	breakSub.stdout.close()
	# Wait for first process to finish
	breakSub.wait()
	# Wait for other processes to finish
	splitSub.wait()
	# Check that processes finished
	print(breakSub.poll())
	print(splitSub.poll())
	
	# Submit batch copy
	bsubCom = 'bsub < job.sh'
	bsubArgs = shlex.split(bsubCom)
	bsubSub = Popen(bsubArgs)

	bsubSub.wait()
	print(bsubSub.poll())

if __name__ == '__main__':
	parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
	Waits for a file to appear.'''))
	# parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('infile',action='store',
			help='SDDS input file.')
	parser.add_argument('outfile',action='store',
			help='SDDS output file.')

	arg=parser.parse_args()
	
	split(arg.verbose,arg.infile,arg.outfile)
