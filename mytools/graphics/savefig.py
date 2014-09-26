import os
import matplotlib.pyplot as plt

def savefig(filename,path="figs"):
	# try:
	#         os.remove(path)
	# except OSError as e:
	#         try:
	#                 os.mkdir(path)
	#         except:
	#                 pass
	if not os.path.exists(path):
		os.makedirs(path)
	filename = ''.join([path,'/',filename])
	plt.savefig('{}.eps'.format(filename).replace(" ","").replace("\n",""))
