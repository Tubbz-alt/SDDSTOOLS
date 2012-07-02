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
			to $NOTIFY_EMAIL if available, user email if not.
	Notifications:
		Notifications are expected to go somewhere.  If no log
		file is specified, notifications must be emailed
		somewhere.  If a log file is specified, the -e option
		will force an email to be sent as well.'''))
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
		help='Requests to disable notification by email.  (Default goes to $NOTIFY_EMAIL or SLAC email account.)')
	parser.add_argument('-e','--email', const=None, default=pelegant.emailprefs(True),
			help='Enables email to be sent.  If there is no option set, tries to send to an email set in environment variable $NOTIFY_EMAIL.  If empty, sends to unix user\'s email.')

	# Concatlte arguments
	parser.add_argument('--il','--inlat','--inlattice',default='facet_v27.3_4mmR56.lte',
		help='Yuri\'s lattice.')
	parser.add_argument('--ol','--outlat','--outlattice',default='run.lte',
		help='Output filename for concatenated lattice.')

	# Parse command line
	arg=parser.parse_args()

	# Switches email to requested
	arg.email.requested=arg.notify

	# Run concatlte
	pelegant.concatlte(arg.il,arg.ol,arg.verbose)

	# Submit Pelegant job
	pelegant.submitPelegant(arg.deck,arg.number,arg.email,arg.log,arg.verbose)
