#!/usr/bin/env python
import argparse
import shlex
from subprocess import *
import shutil
import sys

###########################################
#
# plot_scat.sh
#
# Generates a scatter plot and projection
# plots along the two axes. No fits are
# peformed.
#
# NOTE: Can be used with 'plot_core.sh'.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_scat.sh data.sdds xvar yvar \
#   [xlow] [xhigh] [ylow] [yhigh]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.sdds : SDDS file from which the data
#             is to be extracted. Expected
#             to be output from Elegant.
#             If the file's extension is
#             either '.sdds', or '.out',
#             it may be omitted.
#
# xvar      : Variable to be plotted along
#             the x-axis.
#
# yvar      : Variable to be plotted along
#             the y-axis.
#
# Possible values for 'xvar' and 'yvar':
#   x, xp, y, yp, z, d, t, p
#   where xp = x', yp = y', and d = dp/p
#
# xlow      : Lower bound on x-axis.
#
# xhigh     : Upper bound on x-axis.
#
# ylow      : Lower bound on y-axis.
#
# yhigh     : Upper bound on y-axis.
#
# Units for lower/upper bounds:
#
#   x,y,z: mm
#   xp,yp: mrad
#   d    : %
#   t    : s
#   p    : MeV/c
#
###########################################

ver='1.0'

def plotscat(sddsIn,limits):
	# print sddsIn
	# com="sddsquery -pipe=input"
	# args=shlex.split(com)
	# sqSub = Popen(args,stdin=sddsIn,stdout=sddsOut)

	args=(shlex.split("sddsprocess -pipe=input,output -noWarnings") + 
			["-convertUnits=column,x,mm,m,1.e3"] +
			["-convertUnits=column,xp,mrad,,1.e3"] +
			["-convertUnits=column,y,mm,m,1.e3"] +
			["-convertUnits=column,yp,mrad,,1.e3"] +
			["-process=t,average,tbar"] +
			["-define=column,z,t tbar - 2.99792458E11 *,units=mm"] +
			["-define=column,d,p pCentral - pCentral / 100 *,units=%"])
	sprocSub = Popen(args,stdin=sddsIn,stdout=PIPE)

	if limits!=none:
		filterStr=''
		for i in limits:
			filterStr=filterStr+','i[0]+','+i[1]+','+i[2]
		
		args=(shlex.split('sddsprocess -pipe=input,output -noWarnings' \
 "-process=x,standardDeviation,xrms" \
 "-process=xp,standardDeviation,xprms" \
 "-process=y,standardDeviation,yrms" \
 "-process=yp,standardDeviation,yprms" \
 "-process=z,standardDeviation,zrms" \
 "-process=d,standardDeviation,drms" \
 "-process=t,standardDeviation,trms" \
 "-process=p,standardDeviation,prms"

		


	args=(shlex.split("sddsprocess hey.tmp -pipe=input -noWarnings") +
			["-process=x,standardDeviation,xrms"] +
			["-process=xp,standardDeviation,xprms"] +
			["-process=y,standardDeviation,yrms"] +
			["-process=yp,standardDeviation,yprms"] +
			["-process=z,standardDeviation,zrms"] +
			["-process=d,standardDeviation,drms"] +
			["-process=t,standardDeviation,trms"] +
			["-process=p,standardDeviation,prms"])
	sproc2Sub = Popen(args,stdin=sprocSub.stdout)



class ValidateOtherLimits(argparse.Action):
	def __call__(self,parser,namespace,values,option_string=None):
		# print getattr(namespace,self.dest)
		values[1]=int(values[1])
		values[2]=int(values[2])
		if values[1] >= values[2]:
			msg=option_string + ": the high limit must be greater than the low limit."
			raise argparse.ArgumentError(None,msg)
		app=getattr(namespace,self.dest)
		if app!=None:
			out=app + [values]
		else:
			out=values
		setattr(namespace,'limits',out)
		
class ValidateLimits(argparse.Action):
	def __call__(self,parser,namespace,values,option_string=None):
		# print values
		if values[0] >= values[1]:
			msg=option_string + "the high limit must be greater than the low limit."
			raise argparse.ArgumentError(None,msg)
		else:
			app=getattr(namespace,self.dest)
			columnName = getattr(namespace,option_string[1])
			# print columnName
			# print [columnName] + values
			if app!=None:
				out=[app, [columnName] + values]
			else:
				out=[columnName] + values
			setattr(namespace,self.dest,out)
			

if __name__ == '__main__':
	parser=argparse.ArgumentParser(description=
			'Concatenates lattice files into one file to be used in a Pelegant simulation.')
	parser.add_argument('-V',action='version',version='%(prog)s v' + ver)
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('input',type=argparse.FileType('r'),default=sys.stdin,nargs='?',
			help='Input file (a \"-\" indicates a pipe.)')
	parser.add_argument('-x',metavar='columnName',required=True,
			help='X-axis variable')
	parser.add_argument('-y',metavar='columnName',
			help='Y-axis variable')
	parser.add_argument('-xl',dest='limits',nargs=2,type=float,metavar=('low','high'),action=ValidateLimits,
			help='X Limits')
	parser.add_argument('-yl',dest='limits',nargs=2,type=float,metavar=('low','high'),action=ValidateLimits,
			help='Y Limits')
	parser.add_argument('-lim',dest='limits',nargs=3,metavar=('columnName','low','high'),action=ValidateOtherLimits,
			help='Other limits')

	arg=parser.parse_args()

	# print arg.limits

	plotscat(arg.input,arg.limits)
