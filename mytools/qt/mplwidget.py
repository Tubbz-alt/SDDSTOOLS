from PyQt4 import QtGui,QtCore
import matplotlib as _mpl
# import matplotlib.figure as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as _FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as _NavigationToolbar
import numpy as _np

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
	return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
	return QtGui.QApplication.translate(context, text, disambig)

class Slider_and_Text(QtGui.QWidget):
	valueChanged = QtCore.pyqtSignal(int)

	def __init__(self,parent=None):
		QtGui.QWidget.__init__(self)
		self.hLayout = QtGui.QHBoxLayout()
		self.slider = QtGui.QSlider()

		self.v = QtGui.QIntValidator()
		self.box = QtGui.QLineEdit()
		self.box.setValidator(self.v)

		self.hLayout.addWidget(self.slider)
		self.hLayout.addWidget(self.box)
		self.setLayout(self.hLayout)
		
		self.slider.valueChanged.connect(self._sliderChanged)
		self.box.textChanged.connect(self._textChanged)

	def setMaximum(self,val):
		self.slider.setMaximum(val)
		# self.v = QtGui.QIntValidator(self.slider.minimum(),self.slider.maximum(),parent=None)
		self.v = QtGui.QIntValidator()
		self.v.setRange(self.slider.minimum(),self.slider.maximum())
		self.box.setValidator(self.v)

	def _sliderChanged(self,val):
		self.box.setText(str(val))
		self.valueChanged.emit(val)

	def _textChanged(self,val):
		self.slider.setValue(int(val))

	def setOrientation(self,*args,**kwargs):
		self.slider.setOrientation(*args,**kwargs)

	def setValue(self,val):
		self.slider.setValue(val)
		self.box.setText(str(val))

class Mpl_Plot(_FigureCanvas):
	def __init__(self,parent=None):
		# Initialize things
		self.fig=_mpl.figure.Figure()
		_FigureCanvas.__init__(self,self.fig)
		_FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		_FigureCanvas.updateGeometry(self)

		# Create axes
		self.ax=self.fig.add_subplot(111)

	def _get_img(self):
		return self._image
	def _set_img(self,image):
		self._image = image
		if image != None:
			self._imgplot = self.ax.imshow(image,interpolation='none')
			imagemax = _np.max(_np.max(image))
			print 'Image max is {}.'.format(imagemax)
			self.fig.colorbar(self._imgplot)
	image = property(_get_img,_set_img)

class Mpl_Image(QtGui.QWidget):
	# Signal for when the rectangle is changed
	rectChanged = QtCore.pyqtSignal(_mpl.patches.Rectangle)

	def __init__(self, parent=None, rectbool = True, toolbarbool=False, image=None):
		# Initialize things
		QtGui.QWidget.__init__(self)
		# Add a vertical layout
		self.vLayout = QtGui.QVBoxLayout()
		# Add a figure
		self.fig=_mpl.figure.Figure()
		# Add a canvas containing the fig
		self.canvas = _FigureCanvas(self.fig)
		_FigureCanvas.setSizePolicy(self.canvas,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
		_FigureCanvas.updateGeometry(self.canvas)

		# Setup the layout
		if toolbarbool:
			self.toolbar = _NavigationToolbar(self.canvas,self)
			self.vLayout.addWidget(self.toolbar)
		self.vLayout.addWidget(self.canvas)
		self.setLayout(self.vLayout)

		# Create axes
		self.ax=self.fig.add_subplot(111)

		# Add image
		self.image = image

		# Include rectangle functionality
		if rectbool:
			self.fig.canvas.mpl_connect('button_press_event', self.on_press)
			self.fig.canvas.mpl_connect('button_release_event', self.on_release)


			self.rect = _mpl.patches.Rectangle((-10,0),0,3,facecolor='w',edgecolor='r',alpha=0.5)

			# img = _np.random.randn(10,10)
			# self.ax.imshow(img)
			self.ax.add_patch(self.rect)

	def _get_img(self):
		return self._image
	def _set_img(self,image):
		self._image = image
		if image != None:
			self._imgplot = self.ax.imshow(image,interpolation='none')
			imagemax = _np.max(_np.max(image))
			print 'Image max is {}.'.format(imagemax)
			self.fig.colorbar(self._imgplot)
	image = property(_get_img,_set_img)

	def set_clim(self,clim_min,clim_max):
		if self.image != None:
			self._clim_min = clim_min
			self._clim_max = clim_max
			self._imgplot.set_clim(clim_min,clim_max)

	def on_press(self,event):
		print 'press'
		self.x0 = event.xdata
		self.y0 = event.ydata

	def on_release(self,event):
		print 'release'
		self.x1 = event.xdata
		self.y1 = event.ydata
		self.rect.set_width(self.x1 - self.x0)
		self.rect.set_height(self.y1 - self.y0)
		self.rect.set_xy((self.x0, self.y0))
		self.ax.figure.canvas.draw()

		self.rectChanged.emit(self.rect)
		print self.rect

	def zoom_rect(self,border=0):
		# Get x coordinates
		x0 = self.rect.get_x()
		width = self.rect.get_width()
		x1 = x0+width

		# Get y coordinates
		y0 = self.rect.get_y()
		height = self.rect.get_height()
		y1 = y0+height

		# Add border
		x0 = x0 - border
		x1 = x1 + border
		y0 = y0 - border
		y1 = y1 + border

		# Validate coordinates to prevent unPythonic crash
		if not ((0 <= x0 and x0 <= self.image.shape[1]) and (0 <= x1 and x1 <= self.image.shape[1])):
			print 'X issue'
			x0 = 0
			x1 = self.image.shape[1]
		if not ((0 <= y0 and y0 <= self.image.shape[0]) and (0 <= y1 and y1 <= self.image.shape[0])):
			print 'y issue'
			y0 = 0
			y1 = self.image.shape[0]

		print self.rect
		self.ax.set_xlim(x0,x1)
		self.ax.set_ylim(y0,y1)

class Mpl_Image_Plus_Slider(QtGui.QWidget):
	# def __init__(self, parent=None, **kwargs):
	def __init__(self, parent=None,**kwargs):
		# Initialize self as a widget
		QtGui.QWidget.__init__(self,parent)

		# Add a vertical layout with parent self
		self.vLayout = QtGui.QVBoxLayout(self)
		self.vLayout.setObjectName(_fromUtf8("vLayout"))

		# Add an Mpl_Image widget to vLayout,
		# save it to self._img
		# Pass arguments through to Mpl_Image.
		self._img=Mpl_Image(parent=parent,toolbarbool=True,**kwargs)
		self._img.setObjectName(_fromUtf8("_img"))
		self.vLayout.addWidget(self._img)

		# Add a slider to vLayout,
		# save it to self.max_slider
		# self.max_slider = QtGui.QSlider(self)
		self.max_slider = Slider_and_Text(self)
		self.max_slider.setObjectName(_fromUtf8("max_slider"))
		self.max_slider.setOrientation(QtCore.Qt.Horizontal)
		self.vLayout.addWidget(self.max_slider)

		# Setup slider to work with _img's clims
		self.max_slider.valueChanged.connect(lambda val: self.set_clim(0,val))

	def _get_image(self):
		return self._img.image
	def _set_image(self,image):
		self._img.image = image
		maximage = _np.max(_np.max(image))
		self.max_slider.setMaximum(maximage)
	image = property(_get_image,_set_image)

	def _get_rect(self):
		return self._img.rect
	def _set_rect(self,rect):
		self._img.rect(rect)
	rect = property(_get_rect,_set_rect)

	def zoom_rect(self,border):
		self._img.zoom_rect(border)

	def set_clim(self,clim_min,clim_max):
		self._img.set_clim(0,clim_max)
		self._img.ax.figure.canvas.draw()

	def setSliderValue(self,val):
		self.max_slider.setValue(val)
