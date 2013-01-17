from hist2d import hist2d
from showfig import showfig
from addlabel import addlabel
import graphics

class Error(Exception):
	"""Base class for exceptions in this module."""
	pass

class ArgumentError(Error):
	"""Exception raised for errors in function arguments.

	Attributes:
		arg -- input argument in which the error occurred
		msg -- explanation of the error
	"""

	def __init__(self, arg, msg):
		self.arg = arg
		self.msg = msg
