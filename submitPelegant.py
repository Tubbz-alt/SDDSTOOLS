#!/usr/bin/env python
import argparse
import shlex
from subprocess import call
import os
import sys
import textwrap
import pelegant
from getpass import getuser

def submitPelegant(elefile,cores,email,log,verbose):
	# Setting log options
	if (log!=None):
		logstr=" -oo " + log
		if verbose:
			print("Log file: " + log + " ...")
	else:
		logstr=''
		print("No logfile requested, sending to email.  (Notification mandatory.)")

	if email.requested and verbose:
		print "Email requested."

	options=''
	if logstr=='' or email.requested:
		options = ' -N'
		if email.address!=None:
			options = options + ' -u ' + email.address
			if verbose:
				print "Sending email to " + email.address + '.'
		else:
			print "No email address specified, using LFS email for user " + getuser() + '.'

	if verbose:
		print(textwrap.dedent('''\
				
			Submitting Pelegant run to queue \"beamphysics\":
				Deck file: %s
				Cores: %i''' % (elefile,cores)))
	# Concatenate command
	maincommand="bsub -a mympi -q beamphysics" + logstr + " -n " + str(cores) + options + " Pelegant " + elefile

	# Diagnostic
	# print maincommand

	if not (os.path.isfile(elefile)):
		print("File does not exist: " + elefile)
		sys.exit()
	# Run Command
	call(shlex.split(maincommand))

if __name__ == '__main__':
	parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
	Submits a Pelegant job to the LSF beamphysics queue.

	Notifications:
		Notifications are expected to go somewhere.  If no log
		file is specified, notifications must be emailed
		somewhere.  If a log file is specified, the -e option
		will force an email to be sent as well.'''))
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('-l','--log',nargs='?',const='run.log',help='Log file output. (Default=run.log)')
	parser.add_argument('deck',action='store',nargs='?',default='facet.ele',
			help='Elegant input deck. (Default=facet.ele)')
	parser.add_argument('-n','--number', action='store', type=int, default=8,
			help='Number of cores to use. (Default=8)')
	parser.add_argument('-e','--email', nargs='?', const=None, default=pelegant.emailprefs(), action=pelegant.note_address,
			help='Enables email to be sent.  If there is no option set, tries to send to an email set in environment variable $NOTIFY_EMAIL.  If empty, sends to unix user\'s email.')
			# help='Overrides which email account to send to.  If enabled, overrides notification flag.\n' \
			# 'Searches for email in environment variable $NOTIFY_EMAIL.')

	# Parse command line
	arg=parser.parse_args()

	# Call runElegant with command line
	# arguments/options
	submitPelegant(arg.deck,arg.number,arg.email,arg.log,arg.verbose)
