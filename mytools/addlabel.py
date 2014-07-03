import matplotlib.pyplot as plt

def addlabel(toplabel=None,xlabel=None,ylabel=None,axes=None,clabel=None,cb=None):
	"""Adds labels to a plot."""

	if axes is not None:
		if toplabel is not None:
			axes.set_title(toplabel)
		if xlabel is not None:
			axes.set_xlabel(xlabel)
		if ylabel is not None:
			axes.set_ylabel(ylabel)
		if (clabel is not None) and (cb is not None):
			cb.set_label(clabel)

	if toplabel is not None:
		plt.title(toplabel)
	if xlabel is not None:
		plt.xlabel(xlabel)
	if ylabel is not None:
		plt.ylabel(ylabel)
