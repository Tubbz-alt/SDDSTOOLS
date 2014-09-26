#!/usr/bin/env python
import argparse as _argparse
from sdds2array import sdds2array
from sddshist2d import sddshist2d
from sddsload import sddsload
from showfig import showfig



class ValidateOtherLimits(_argparse.Action):
	def __call__(self,parser,namespace,values,option_string=None):
		# print getattr(namespace,self.dest)
		values[1]=int(values[1])
		values[2]=int(values[2])
		if values[1] >= values[2]:
			msg=option_string + ": the high limit must be greater than the low limit."
			raise _argparse.ArgumentError(None,msg)
		app=getattr(namespace,self.dest)
		if app!=None:
			out=app + [values]
		else:
			out=[values]
		setattr(namespace,'limits',out)
		
class ValidateLimits(_argparse.Action):
	def __call__(self,parser,namespace,values,option_string=None):
		# print values
		if values[0] >= values[1]:
			msg=option_string + "the high limit must be greater than the low limit."
			raise _argparse.ArgumentError(None,msg)
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

__all__=["addlabels","hist2d","sdds2array","sddshist2d","sddsload","showfig"]
