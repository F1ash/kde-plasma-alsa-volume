#  ColorWidget.py
#  
#  Copyright 2013 Flash <kaperang07@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

from PyQt4.QtCore import QString, SIGNAL
from PyQt4.QtGui import *
from TestSliders import TestSliders

class ColorWidget(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = obj.Settings
		self.obj = obj
		if not parent : return

		self.colourIcon = QIcon().fromTheme('color')

		self.testSliders = TestSliders(obj, self)

		self.layout = QGridLayout()

		self.fontColourLabel = QLabel('fontColour :')
		self.layout.addWidget(self.fontColourLabel, 0, 0)
		self.fontColourButton = QPushButton(self.colourIcon, '')
		self.fontColourButton.setMaximumWidth(30)
		self.fontColourButton.setToolTip('Slider Shield Font Color')
		self.connect(self.fontColourButton, SIGNAL('clicked()'), self.fontColour)
		self.layout.addWidget(self.fontColourButton, 0, 1)

		self.sliderColour1Label = QLabel('sliderColour1 :')
		self.layout.addWidget(self.sliderColour1Label, 1, 0)
		self.sliderColour1Button = QPushButton(self.colourIcon, '')
		self.sliderColour1Button.setMaximumWidth(30)
		self.sliderColour1Button.setToolTip('Background Slider Color')
		self.connect(self.sliderColour1Button, SIGNAL('clicked()'), self.sliderColour1)
		self.layout.addWidget(self.sliderColour1Button, 1, 1)

		self.sliderColour2Label = QLabel('sliderColour2 :')
		self.layout.addWidget(self.sliderColour2Label, 2, 0)
		self.sliderColour2Button = QPushButton(self.colourIcon, '')
		self.sliderColour2Button.setMaximumWidth(30)
		self.sliderColour2Button.setToolTip('Slider Color')
		self.connect(self.sliderColour2Button, SIGNAL('clicked()'), self.sliderColour2)
		self.layout.addWidget(self.sliderColour2Button, 2, 1)

		self.handlerColourLabel = QLabel('handlerColour :')
		self.layout.addWidget(self.handlerColourLabel, 3, 0)
		self.handlerColourButton = QPushButton(self.colourIcon, '')
		self.handlerColourButton.setMaximumWidth(30)
		self.handlerColourButton.setToolTip('handler Color')
		self.connect(self.handlerColourButton, SIGNAL('clicked()'), self.handlerColour)
		self.layout.addWidget(self.handlerColourButton, 3, 1)

		self.layout.addWidget(self.testSliders, 4, 0, 6, 1)

		self.setLayout(self.layout)
		self.restoreValues()

	def initValue(self, key_, default = '0'):
		if self.Settings.contains(key_) :
			#print key_, Settings.value(key_).toString()
			return self.Settings.value(key_).toString()
		else :
			if default == '0' :
				default = self.getSystemColor('int')
			self.Settings.setValue(key_, QVariant(default))
			#print key_, Settings.value(key_).toString()
			return default

	def restoreValues(self):
		self.fontColourVar = self.initValue('fontColour')
		self.sliderColour1Var = self.initValue('sliderColour1', 1355022335)
		self.sliderColour2Var = self.initValue('sliderColour2', 1355022335)
		self.handlerColourVar = self.initValue('handlerColour', 1355022335)
		
		self.fontColourLabel.setStyleSheet(self.getRGBaStyle((QString(self.fontColourVar).toUInt()[0], True)))
		self.sliderColour1Label.setStyleSheet(self.getRGBaStyle((QString(self.sliderColour1Var).toUInt()[0], True)))
		self.sliderColour2Label.setStyleSheet(self.getRGBaStyle((QString(self.sliderColour2Var).toUInt()[0], True)))
		self.handlerColourLabel.setStyleSheet(self.getRGBaStyle((QString(self.handlerColourVar).toUInt()[0], True)))

	def setSlidersColor(self, get_Style = None):
		sliderColour1 = self.getRGBaStyle((QString(self.sliderColour1Var).toUInt()[0], True), 'slider')
		sliderColour2 = self.getRGBaStyle((QString(self.sliderColour2Var).toUInt()[0], True), 'slider')
		handlerColour = self.getRGBaStyle((QString(self.handlerColourVar).toUInt()[0], True), 'slider')
		
		return self.testSliders.setSlidersColor(sliderColour1, sliderColour2, handlerColour, get_Style)


	def getSystemColor(self, key_ = ''):
		currentBrush = QPalette().buttonText()
		colour = currentBrush.color()
		if key_ == 'int' :
			# print colour.rgba()
			return colour.rgba()
		else :
			return str(colour.getRgb())

	def getRGBaStyle(self, (colour, yes), str_ = 'label'):
		if yes :
			if str_ == 'label' :
				style = 'QLabel { color: rgba' + str(QColor().fromRgba(colour).getRgb()) + ';} '
			else :
				style = 'rgba' + str(QColor().fromRgba(colour).getRgb())
		else :
			if str_ == 'label' :
				style = 'QLabel { color: rgba' + self.getSystemColor() + ';} '
			else :
				style = 'rgba' + self.getSystemColor()
		return style

	def getColour(self, (currentColour, yes)):
		colour = QColorDialog()
		selectColour, _yes = colour.getRgba(currentColour)
		colour.done(0)
		return str(selectColour), _yes, self.getRGBaStyle((selectColour, _yes))

	def fontColour(self):
		colour, yes, style = self.getColour(QString(self.fontColourVar).toUInt())
		if yes :
			self.fontColourVar = colour
			self.fontColourLabel.clear()
			self.fontColourLabel.setStyleSheet(style)
			self.fontColourLabel.setText('fontColour :')

	def sliderColour1(self):
		colour, yes, style = self.getColour(QString(self.sliderColour1Var).toUInt())
		if yes :
			self.sliderColour1Var = colour
			self.sliderColour1Label.clear()
			self.sliderColour1Label.setStyleSheet(style)
			self.sliderColour1Label.setText('sliderColour1 :')
			self._updateStyle()

	def sliderColour2(self):
		colour, yes, style = self.getColour(QString(self.sliderColour2Var).toUInt())
		if yes :
			self.sliderColour2Var = colour
			self.sliderColour2Label.clear()
			self.sliderColour2Label.setStyleSheet(style)
			self.sliderColour2Label.setText('sliderColour2 :')
			self._updateStyle()

	def handlerColour(self):
		colour, yes, style = self.getColour(QString(self.handlerColourVar).toUInt())
		if yes :
			self.handlerColourVar = colour
			self.handlerColourLabel.clear()
			self.handlerColourLabel.setStyleSheet(style)
			self.handlerColourLabel.setText('handlerColour :')
			self._updateStyle()

	def _updateStyle(self):
		self.testSliders.setSlidersStyleSheet()
		self.obj.sizeSelect.testSliders.setSlidersStyleSheet()

	def refreshInterfaceSettings(self):
		self.Settings.setValue('fontColour', self.fontColourVar)
		self.Settings.setValue('sliderColour1', self.sliderColour1Var)
		self.Settings.setValue('sliderColour2', self.sliderColour2Var)
		self.Settings.setValue('handlerColour', self.handlerColourVar)
		self.Settings.sync()
