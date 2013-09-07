import matplotlib.pyplot as _plt

# Show and configure any figure
def showfig(fig=_plt.gcf()):
	ax=fig.gca()
	# Swap y axis if needed
	alim=list(ax.axis())
	if alim[3]<alim[2]:
		temp=alim[2]
		alim[2]=alim[3]
		alim[3]=temp
		ax.axis(alim)
	ax.set_aspect('auto')
	fig.show()
