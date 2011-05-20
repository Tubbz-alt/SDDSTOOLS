#!/usr/bin/env python
import argparse
import shlex
from subprocess import call
import os

def submitPelegant(elefile,cores,notify,email,log,verbose):
	# Setting notify options
	if verbose & (notify | (log==None)):
		if email!=None:
			print("Job completion email to: " + email + " ...")
		else:
			print("Job completion email to user email ...")
	options=""
	if notify: options=options + " -N"

	# Change email if given
	if email!=None: options=options + " -u " + email

	# Setting log options
	if verbose & (log!=None): print("Log file: " + log + " ...")
	logstr='' if log==None else " -oo " + log

	# Concatenate command
	maincommand="bsub -a mympi -q beamphysics" + logstr + " -n " + str(cores) + options + " Pelegant " + elefile

	# Diagnostic
	print maincommand

	# Run Command
	# call(shlex.split(maincommand))

if __name__ == '__main__':
	import pelegant
	try:
		email=os.environ['OTIFY_EMAIL']
	except:
		email=None
	
	parser=argparse.ArgumentParser(description='Submits Pelegant jobs to LSF queue beamphysics.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('-l','--log',nargs='?',const='run.log',help='Log file output.')
	parser.add_argument('deck',action='store',nargs='?',default='facet.ele',
			help='Elegant input deck.')
	parser.add_argument('-n','--number', action='store', type=int, default=10,
			help='Number of cores to use.')
	parser.add_argument('-N','--notify', action='store_true',default=False,
			help='Enable notification by email.  (Default goes to SLAC email account.)')
	# Email argument must come after notify
	# as it changes it in certain cases.
	parser.add_argument('-e','--email', nargs='?', action=pelegant.note_address,
			help='Overrides which email account to send to.  If enabled, overrides notification flag.\n' \
			'Searches for email in environment variable $NOTIFY_EMAIL.')

	# Parse command line
	arg=parser.parse_args()

	# Call runElegant with command line
	# arguments/options
	submitPelegant(arg.deck,arg.number,arg.notify,arg.email,arg.log,arg.verbose)
