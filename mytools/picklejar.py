import cPickle

class PickleJar(object):
	def __init__(self,**kwargs):
		for name,value in kwargs.items():
			setattr(self,name,value)

def picklejar(filename,**kwargs):
	print "Pickling..."
	f = open(filename,'wb')
	out = PickleJar(**kwargs)
	cPickle.dump(out,f,protocol=-1)
	f.close()
	print "Finished pickling!"

