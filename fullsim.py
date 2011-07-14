#!/usr/bin/env python
import argparse
import os
import pelegant
import textwrap

if __name__ == '__main__':
	parser=argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
		description=textwrap.dedent('''\
	Runs a complete Pelegant simulation, including
	concatenating lattice files and submitting a Pelegant job.

	Default behavior is to run in verbose mode:
		First:  Concatenate prepend.lte, facet_v27.3_4mmR56.lte, 
		        and append.lte into run.lte
		Second: Run Pelegant on facet.ele with 10 cores, 
		        output written to run.log, and email sent
			to $NOTIFY_EMAIL if available, user email if not.'''))
	# ==========================================
	# ==========================================
	#   All arguments should be OPTIONAL
	#   but never allowed to be BLANK.
	#   Things don't necessarily follow
	#   bsub conventions!
	# ==========================================
	# ==========================================
	# Basic Arguments
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('--dv','--verbose',dest='verbose', action='store_false', help='Disable verbose mode.')

	# submitPelegant options
	parser.add_argument('-l','--log',default='run.log',
		help='Log file output.')
	parser.add_argument('-d','--deck',default='facet.ele',
		help='Elegant input deck.')
	parser.add_argument('-n','--number',type=int, default=10,
		help='Number of cores to use.')
	parser.add_argument('--dN','--disablenotify',dest='notify',action='store_false',default=True,
		help='Disable notification by email.  (Default goes to $NOTIFY_EMAIL or SLAC email account.)')
	try:
		notifyEmail=os.environ['NOTIFY_EMAIL']
	except:
		notifyEmail=None;
	parser.add_argument('-e','--email',default=notifyEmail,
		help='Overrides which email account to send to.  Default is to try to send to $NOTIFY_EMAIL.  Use --dN to disable email.')

	# Concatlte arguments
	parser.add_argument('--il','--inlat','--inlattice',default='facet_v27.3_4mmR56.lte',
		help='Yuri\'s lattice.')
	parser.add_argument('--ol','--outlat','--outlattice',default='run.lte',
		help='Output filename for concatenated lattice.')

	# Parse command line
	arg=parser.parse_args()

	# Run concatlte
	pelegant.concatlte(arg.il,arg.ol,arg.verbose)

	# Tries to get email from $NOTIFY_EMAIL

	# Submit Pelegant job
	pelegant.submitPelegant(arg.deck,arg.number,arg.notify,arg.email,arg.log,arg.verbose)
