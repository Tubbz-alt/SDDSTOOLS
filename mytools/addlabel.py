import matplotlib.pyplot as plt

def addlabel(toplabel=None,xlabel=None,ylabel=None,axes=None):
	"""Adds labels to a plot."""

	if toplabel is not None:
		plt.title(toplabel)
	if xlabel is not None:
		plt.xlabel(xlabel)
	if ylabel is not None:
		plt.ylabel(ylabel)
