#!/usr/bin/env python
import os
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

def plotscat(sddsIn,xCoord,yCoord,limits):
	args=(shlex.split("sddsprocess -pipe=input,output -noWarnings") + 
			["-convertUnits=column,x,mm,m,1.e3"] +
			["-convertUnits=column,xp,mrad,,1.e3"] +
			["-convertUnits=column,y,mm,m,1.e3"] +
			["-convertUnits=column,yp,mrad,,1.e3"] +
			["-process=t,average,tbar"] +
			["-define=column,z,t tbar - 2.99792458E11 *,units=mm"] +
			["-define=column,d,p pCentral - pCentral / 100 *,units=%"])
	sprocSub = Popen(args,stdin=sddsIn,stdout=PIPE)

	inPipe=sprocSub.stdout

	if limits!=None:
		filterStr='-filter=column'

		for i in limits:
			filterStr=filterStr + ',' + i[0] + ',' + str(i[1]) + ',' + str(i[2])

		if len(limits)>1:
			filterStr = filterStr + ',&'
		
	else:
		filterStr=''
		outPipe=inPipe

	args=(shlex.split('sddsprocess -pipe=input,output -noWarnings ' + filterStr) +
		["-process=x,standardDeviation,xrms"] +
		["-process=xp,standardDeviation,xprms"] +
		["-process=y,standardDeviation,yrms"] +
		["-process=yp,standardDeviation,yprms"] +
		["-process=z,standardDeviation,zrms"] +
		["-process=d,standardDeviation,drms"] +
		["-process=t,standardDeviation,trms"] +
		["-process=p,standardDeviation,prms"] )

	filtSub=Popen(args,stdin=inPipe,stdout=PIPE)
	outPipe=filtSub.stdout

	args=(shlex.split("sddsprocess -pipe=input,output -noWarnings") +
			["-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV"] +
			["-process=E,average,Ebar"] +
			["-print=param,ELabel,E+$b0+$n=%.3g %s,Ebar,Ebar.units"] +
			["-print=param,xrmsLabel,+$gs+$r+$bx+$n=%.3g %s,xrms,xrms.units"] +
			["-print=param,xprmsLabel,+$gs+$r+$bxp+$n=%.3g %s,xprms,yprms.units"] +
			["-print=param,yrmsLabel,+$gs+$r+$by+$n=%.3g %s,yrms,yrms.units"] +
			["-print=param,yprmsLabel,+$gs+$r+$byp+$n=%.3g %s,yprms,yprms.units"] +
			["-print=param,zrmsLabel,+$gs+$r+$bz+$n=%.3g %s,zrms,zrms.units"] +
			["-print=param,drmsLabel,+$gs+$r+$b+$gd+$r+$n=%.3g %s,drms,drms.units"] +
			["-print=param,trmsLabel,+$gs+$r+$bt+$n=%.3g %s,trms,trms.units"] +
			["-print=param,prmsLabel,+$gs+$r+$bp+$n=%.3g %s,prms,prms.units"] +
			["-print=param,xLabel,x (%s),x.units"] +
			["-print=param,xpLabel,x' (%s),xp.units"] +
			["-print=param,yLabel,y (%s),y.units"] +
			["-print=param,ypLabel,y' (%s),yp.units"] +
			["-print=param,zLabel,z (%s),z.units"] +
			["-print=param,dLabel,+$gd+$rp/p (%s),d.units"] +
			["-print=param,tLabel,t (%s),t.units"] +
			["-print=param,pLabel,p (%s),p.units"] )
	sproc3Sub = Popen(args,stdin=outPipe,stdout=PIPE)

	hists=[xCoord, yCoord]
	fid=open('hey.out','w')
	histProc=[fid]
	otherProc=[]
	for i in hists:
		histArgs=shlex.split("sddshist hey." + i + "his -pipe=input -data=" + i + " -bin=100")
		tmpProc=Popen(histArgs,stdin=PIPE)
		histProc=histProc+ [tmpProc.stdin]
		otherProc=otherProc + [tmpProc]
	while sproc3Sub.poll() == None:
		buf=os.read(sproc3Sub.stdout.fileno(),10000)
		for proc in histProc:
			proc.write(buf)
	fid.close()
	for proc in otherProc:
		proc.stdin.close()
	
	plotArgs=(shlex.split("sddsplot -groupby=fileindex " +
			"-split=page -sep=tag " +
			"-layout=2,2,limit=3 " +
			"-column=" + xCoord + "," + yCoord + " hey.out " +
			"-graph=dot,type=3 " +
			"-tag=1 -sparse=1 -topline=@ELabel " +
			"-xlabel=@" + xCoord + "Label -ylabel=@" + yCoord + "Label " +
			"-column=frequency," + yCoord + " hey." + yCoord + "his " +
			"-graph=yimpulse,type=2 -unsup=x -xlabel=N " +
			"-tag=2 -ylabel=@" + yCoord + "Label " +
			"-column=" + xCoord + ",frequency hey." + xCoord + "his " +
			"-graph=impulse,type=1 -unsup=y -ylabel=N " +
			"-tag=3 -xlabel=@" + xCoord + "Label"))
	
	# print plotArgs

	Popen(plotArgs)


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
			out=[values]
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
				out=app + [[columnName] + values]
			else:
				out=[[columnName] + values]
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

	plotscat(arg.input,arg.x,arg.y,arg.limits)
