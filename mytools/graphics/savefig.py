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
	final_filename = os.path.abspath(final_filename)
	final_dir = os.path.dirname(final_filename)
	
	if not os.path.exists(final_dir):
		os.makedirs(final_dir)

	if fig is not None:
		fig.savefig(final_filename,bbox_inches='tight',**kwargs)
	else:
		plt.savefig(final_filename,bbox_inches='tight',**kwargs)
