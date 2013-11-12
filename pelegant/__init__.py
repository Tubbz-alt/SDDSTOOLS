#!/usr/bin/env python
import os
import argparse
from concatlte import concatlte
from submitPelegant import submitPelegant


__all__=["submitPelegant","concatlte"]


def checkvar(envvar):
	try:
		value=os.environ[envvar]
	except:
		value=None
	# print(value)
	return value

# Email variable class
class emailprefs:
	# print(requested)
	# print(value)
	# raise argparse.ArgumentTypeError('hi')
	"""Preferences for email notification."""
	def __init__(self,requested=False,environvar=None,value=None):
		self.requested = requested
		self.environvar=environvar
		if value==None:
			self.value = checkvar(environvar)
		else:
			self.value = value
		if self.value==None:
			self.value = os.environ['PHYSICS_USER']
			print 'Using current fphysics login: ' + self.value

		# raise ValueError('problem')

# Adds action to load email from $NOTIFY_EMAIL if possible
class note_address(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		# print getattr(namespace,self.dest).environvar
		# print values
		if values==None:
			out=emailprefs(True,getattr(namespace,self.dest).environvar)
		else:
			out=emailprefs(True,getattr(namespace,self.dest).environvar,values)
		setattr(namespace, self.dest, out)
