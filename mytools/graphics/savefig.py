import os
import matplotlib.pyplot as plt

def savefig(filename,path="figs",fig=None,ext='eps',**kwargs):
	# try:
	#         os.remove(path)
	# except OSError as e:
	#         try:
	#                 os.mkdir(path)
	#         except:
	#                 pass
	if not os.path.exists(path):
		os.makedirs(path)

	filename       = ''.join([path,'/',filename])
	final_filename = '{}.{}'.format(filename,ext).replace(" ","").replace("\n","")

	if fig != None:
		fig.savefig(final_filename,**kwargs)
	else:
		plt.savefig(final_filename,**kwargs)
