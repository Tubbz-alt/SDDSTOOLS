#!/usr/bin/env python
import argparse
import os
import shlex
from subprocess import call
import shutil
from glob import glob

def plotscat(inputfile,xaxis,yaxis,his,clip,verbose):
	data_base, data_ext = os.path.splitext(inputfile)

	lengthvars = ['x','y']
	anglevars = ['xp','yp']
	timevars = ['t','z']
	pvars = ['d']

	# Unit conversion/definitions
	convertStr = ""
	rmsStr = ""
	labelStr = ""

	for i in [xaxis,yaxis]:
		rmsStr = rmsStr +  " -process=" + i + ",standardDeviation," + i + "rms"
		convert = True
		if i in lengthvars:
			convertStr = convertStr + " \"-convertUnits=column," + i + ",mm,m,1.e3\""
		elif i in anglevars:
			convertStr = convertStr + " \"-convertUnits=column," + i + ",mrad,,1.e3\""
		elif i in timevars:
			convertStr = convertStr + " \"-process=t,average,tbar\" \
					\"-define=column,z,t tbar - 2.99792458E11 *,units=mm\""
		elif i in pvars:
			convertStr = convertStr + " \"-define=column,d,p pCentral - pCentral / 100 *,units=%\""
		else:
			convert = False

	if convert:
		command = "sddsprocess " + inputfile + " " + data_base + ".tmp -noWarnings" + convertStr
		if verbose:
			print command
			# print shlex.split(command)
		call(shlex.split(command))
	else:
		shutil.copyfile(inputfile,data_base + ".tmp")

	# Try to find energy.
 	command = "sddsprocess " + data_base + ".tmp \"-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV\" \
			\"-process=E,average,Ebar\" \
			\"-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units\" \
			-noWarnings"
	fnull = open(os.devnull,'w')

	if verbose:
		print command
	try:
		energyerr = call(shlex.split(command),stdout=fnull,stderr=fnull)
	except:
		pass
	fnull.close()

	# RMS calculations
	command = "sddsprocess " + data_base + ".tmp -noWarnings" + rmsStr
	if verbose:
		print shlex.split(command)

	# Create histograms
	if his:
		for i in [xaxis,yaxis]:
			command = "sddshist " + data_base + ".tmp " + data_base + "." + i + "his -data=" + i + " -bin=100"
			if verbose:
				print command
			call(shlex.split(command))

	# Try to create an energy label
	if energyerr==0:
		energystr = " -topline=@ELabel"
	else:
		energystr = ""

	# Plot things
	if his:
		command = "sddsplot -groupby=fileindex \
			  -split=page -sep=tag \
			  -layout=2,2,limit=3 \
			  -column=" + xaxis + "," + yaxis + " " + data_base + ".tmp -graph=dot,type=3 \
			      -tag=1 -sparse=1" + energystr + " \
			  -column=frequency," + yaxis + " " + data_base + "." + yaxis + "his \
			      -graph=yimpulse,type=2 -unsup=x \
			      -tag=2 -xlabel=N \
			  -column=" + xaxis + ",frequency " + data_base + "." + xaxis + "his \
			      -graph=impulse,type=1 -unsup=y \
			      -tag=3 -ylabel=N"
	else:
		command = "sddsplot -groupby=fileindex \
			  -split=page -sep=tag \
			  -column=" + xaxis + "," + yaxis + " " + data_base + ".tmp -graph=dot,type=3 \
			      -sparse=1" + energystr
	if verbose:
		print shlex.split(command)
	call(shlex.split(command))

	# Remove files
	tempfiles = glob(data_base + '.tmp') + glob(data_base + '.tmp~') + glob(data_base + '*.his') + glob('tmp*.1')
	for i in tempfiles:
		os.remove(i)

if __name__ == '__main__':

	parser=argparse.ArgumentParser(description=
			'Scatter-plots a SDDS file.')
	parser.add_argument('-V',action='version',version='%(prog)s v0.1')
	parser.add_argument('-v','--verbose',action='store_true',
			help='Verbose mode.')
	parser.add_argument('inputfile',
			help='Input CSV file.')

	choicesArr=['x','xp','y','yp','z','s','t','d','Particles']

	parser.add_argument('xaxis', choices=choicesArr,
			help='X Axis Variable (Must be SDDS column)')
	parser.add_argument('yaxis', choices=choicesArr,
			help='y Axis Variable (Must be SDDS column)')
	parser.add_argument('--nohis', dest='his', action='store_false',
			help='Don\'t create histograms')
	parser.add_argument('-c','--clip',action='store_true',
			help='Clip tails.')
	arg=parser.parse_args()

	plotscat(arg.inputfile,arg.xaxis,arg.yaxis,arg.his,arg.clip,arg.verbose)
