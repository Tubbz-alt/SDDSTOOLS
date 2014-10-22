import sys
from PyQt4 import QtGui

def get_app(argv=[sys.argv[0]]):
	app = QtGui.QApplication.instance()
	if not app:
		app = QtGui.QApplication(argv)
	return app
