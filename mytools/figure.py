from matplotlib.pyplot import figure as _figure
def figure(title=None):
	fig=_figure()
	if title != None:
		fig.canvas.set_window_title(title)
	return fig
