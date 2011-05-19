#!/usr/bin/env python
import argparse
import shlex
from subprocess import call
import os


def runElegant(elefile,cores,notify,email,log,verbose):
	if verbose: print("Email notification to " + email + "...\nRunning " + elefile + " with Pelegant...")
	options=""
	if notify: options=options + " -N"
	if email!=None: options=options + " -u " + email
	maincommand="bsub -a mympi -q beamphysics -oo " + log + " -n " + str(cores) + options + " Pelegant " + elefile
	# print maincommand
	call(shlex.split(maincommand))

class note_address(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if values==None:
			try:
				values=os.environ['NOTIFY_EMAIL']
				namespace.notify=True
			except:
				raise argparse.ArgumentError(self,'expected one argument ($NOTIFY_EMAIL not set)')
		setattr(namespace, self.dest, values)

if __name__ == '__main__':
	try:
		email=os.environ['OTIFY_EMAIL']
	except:
		email=None
	
	parser=argparse.ArgumentParser(description='Process command line.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose', action='store_true', help='Verbose mode.')
	parser.add_argument('-l','--log',default='run.log',help='Log file output.')
	parser.add_argument('deck',action='store',nargs='?',default='facet.ele',
			help='Elegant input deck.')
	parser.add_argument('-n','--number', action='store', type=int, default=10,
			help='Number of cores to use.')
	parser.add_argument('-N','--notify', action='store_true',default=False,
			help='Enable notification by email.  (Default goes to SLAC email account.)')
	parser.add_argument('-e','--email', nargs='?', action=note_address,
			help='Overrides which email account to send to.  If enabled, overrides notification flag.\n' \
			'Searches for email in environment variable $NOTIFY_EMAIL.')
	arg=parser.parse_args()
	runElegant(arg.deck,arg.number,arg.notify,arg.email,arg.log,arg.verbose)
