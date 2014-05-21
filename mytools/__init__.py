from hist import hist
from hist2d import hist2d
from showfig import showfig
from addlabel import addlabel
from gaussfit import gaussfit
from gaussfit import _gauss
from gaussfit import _gaussvar
from chisquare import chisquare
from curve_fit_unscaled import curve_fit_unscaled
from plot_featured import plot_featured
# import graphics
from figure import figure
from linspacestep import linspacestep
from findpinch import findpinch
from derefdataset import *
from fitimageslice import fitimageslice
import E200
import qt
from Rectangle import Rectangle

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
