#!/usr/bin/env python
import argparse
import shlex
from subprocess import call
import os


def runElegant(elefile,cores,notify,email,verbose):
	if verbose: print("Email notification to " + email + "...\nRunning " + elefile + " with Pelegant...")
	options=""
	if notify: options=options + " -N"
	if email!=None: options=options + " -u " + email
	maincommand="bsub -a mympi -q beamphysics -oo run.log -n " + str(cores) + options + " Pelegant " + elefile
	call(shlex.split(maincommand))

class myAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if values==None:
			try:
				values=os.environ['NOTIFY_EMAIL']
			except:
				raise argparse.ArgumentError(self,'unable to retrieve e-mail, no argument given')
		setattr(namespace, self.dest, values)

if __name__ == '__main__':
	try:
		email=os.environ['OTIFY_EMAIL']
	except:
		email=None
	
	parser=argparse.ArgumentParser(description='Process command line.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('deck',action='store',
			help='Elegant input deck.')
	parser.add_argument('-n','--number', action='store', type=int, default=10,
			help='Number of cores to use.')
	parser.add_argument('-N','--notify', action='store_true',default=False,
			help='Enable notification by email.  (Default goes to SLAC email account.)')
	# parser.add_argument('-e','--email', nargs='?',const=email,
	#                 help='Overrides which email account to send to.  If enabled, overrides notification flag.\n' \
	#                 'Searches for email in environment variable $NOTIFY_EMAIL.')
	parser.add_argument('-e','--email', nargs='?', action=myAction,
			help='Overrides which email account to send to.  If enabled, overrides notification flag.\n' \
			'Searches for email in environment variable $NOTIFY_EMAIL.')
	arg=parser.parse_args()
	# if arg.email==None:
	#         raise argparse.ArgumentError('default','expected at least one argument')
	# else:
	#         arg.notify=True
	runElegant(arg.deck,arg.number,arg.notify,arg.email,arg.verbose)
