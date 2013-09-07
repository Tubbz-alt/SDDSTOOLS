import sdds as _sdds

def sddsload(filename):
	this=_sdds.SDDS(0)
	this.load(filename)
	return this
