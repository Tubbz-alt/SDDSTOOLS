#!/usr/bin/env python
import os
import argparse
from concatlte import concatlte
from submitPelegant import submitPelegant

__all__=["submitPelegant","concatlte"]

# Adds action to load email from $NOTIFY_EMAIL if possible
class note_address(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if values==None:
			try:
				# Looks for $NOTIFY_EMAIL
				values=os.environ['NOTIFY_EMAIL']
				# Turns notifications on
				namespace.notify=True
			except:
				raise argparse.ArgumentError(self,'expected one argument ($NOTIFY_EMAIL not set)')
		setattr(namespace, self.dest, values)
