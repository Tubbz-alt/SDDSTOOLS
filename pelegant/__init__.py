#!/usr/bin/env python
import os
import argparse
from concatlte import concatlte
from submitPelegant import submitPelegant

__all__=["submitPelegant","concatlte"]

notifyvar='NOTIFY_EMAIL'

def email():
	try:
		value=os.environ[notifyvar]
	except:
		value=None
	
	return value

# Email variable class
class emailprefs:
	"""Preferences for email notification."""
	def __init__(self,requested=False,address=email()):
		self.requested = requested
		self.address   = address

# Adds action to load email from $NOTIFY_EMAIL if possible
class note_address(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if values==None:
			out=emailprefs(True)
		else:
			out=emailprefs(True,values)
		setattr(namespace, self.dest, out)
