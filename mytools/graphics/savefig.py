import os
import matplotlib.pyplot as plt

def savefig(elepath,top):
	try:
		os.remove(elepath)
	except OSError as e:
		# pass
		try:
			os.mkdir(elepath)
		except:
			pass
	top = ''.join([elepath,'/',top])
	plt.savefig('{}.eps'.format(top).replace(" ","").replace("\n",""))
