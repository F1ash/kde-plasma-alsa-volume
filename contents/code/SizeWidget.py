#  SizeWidget.py
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

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QSpinBox, QGridLayout
from TestSliders import TestSliders

class SizeWidget(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = obj.Settings
		self.obj = obj

		self.Settings.beginGroup("Size")
		self.marginVar = self.Settings.value('Margin', 3).toString()
		self.thicknessVar = self.Settings.value('Thickness', 5).toString()
		self.handlerThicknessVar = self.Settings.value('HThickness', 5).toString()
		self.handlerLedgeVar = self.Settings.value('HLedge', 3).toString()
		self.Settings.endGroup()

		self.testSliders = TestSliders(obj, self)
		self.VBLayout = QGridLayout()
		
		self.marginBox = QSpinBox()
		self.marginBox.setToolTip("Margin around slider")
		self.marginBox.setMinimum(3)
		self.marginBox.setMaximum(400)
		self.marginBox.setSingleStep(1)
		self.VBLayout.addWidget(self.marginBox, 0, 0)
		
		self.thicknessBox = QSpinBox()
		self.thicknessBox.setToolTip("Thickness of slider")
		self.thicknessBox.setMinimum(5)
		self.thicknessBox.setMaximum(400)
		self.thicknessBox.setSingleStep(1)
		self.VBLayout.addWidget(self.thicknessBox, 0, 1)
		
		self.handlerThicknessBox = QSpinBox()
		self.handlerThicknessBox.setToolTip("Thickness of handler")
		self.handlerThicknessBox.setMinimum(5)
		self.handlerThicknessBox.setMaximum(100)
		self.handlerThicknessBox.setSingleStep(1)
		self.VBLayout.addWidget(self.handlerThicknessBox, 1, 0)
		
		self.handlerLedgeBox = QSpinBox()
		self.handlerLedgeBox.setToolTip("Ledge of handler")
		self.handlerLedgeBox.setMinimum(3)
		self.handlerLedgeBox.setMaximum(100)
		self.handlerLedgeBox.setSingleStep(1)
		self.VBLayout.addWidget(self.handlerLedgeBox, 1, 1)

		self.VBLayout.addWidget(self.testSliders, 2, 0, 3, 2, Qt.AlignCenter)

		self.setLayout(self.VBLayout)
		self.restoreValues()
		self.marginBox.valueChanged[int].connect(self.marginSet)
		self.thicknessBox.valueChanged[int].connect(self.thicknessSet)
		self.handlerThicknessBox.valueChanged[int].connect(self.handlerThicknessSet)
		self.handlerLedgeBox.valueChanged[int].connect(self.handlerLedgeSet)

	def restoreValues(self):
		self.Settings.beginGroup("Size")
		self.marginVar = self.Settings.value('Margin', 3).toString()
		self.thicknessVar = self.Settings.value('Thickness', 5).toString()
		self.handlerThicknessVar = self.Settings.value('HThickness', 5).toString()
		self.handlerLedgeVar = self.Settings.value('HLedge', 3).toString()
		self.Settings.endGroup()
		
		self.marginBox.setValue(int(self.marginVar))
		self.thicknessBox.setValue(int(self.thicknessVar))
		self.handlerThicknessBox.setValue(int(self.handlerThicknessVar))
		self.handlerLedgeBox.setValue(int(self.handlerLedgeVar))

	def marginSet(self, value = 0):
		self.marginVar = str(value)
		self._updateStyle()
	def thicknessSet(self, value = 0):
		self.thicknessVar = str(value)
		self._updateStyle()
	def handlerThicknessSet(self, value = 0):
		self.handlerThicknessVar = str(value)
		self._updateStyle()
	def handlerLedgeSet(self, value = 0):
		self.handlerLedgeVar = str(value)
		self._updateStyle()

	def _updateStyle(self):
		self.testSliders.setSlidersStyleSheet()
		self.obj.colorSelect.testSliders.setSlidersStyleSheet()

	def setSlidersSize(self, get_Style = None):
		return self.testSliders.setSlidersSize(\
			self.marginVar, self.thicknessVar, \
			self.handlerThicknessVar, \
			self.handlerLedgeVar, get_Style)

	def refreshInterfaceSettings(self):
		self.Settings.beginGroup("Size")
		self.Settings.setValue('Margin', self.marginVar)
		self.Settings.setValue('Thickness', self.thicknessVar)
		self.Settings.setValue('HThickness', self.handlerThicknessVar)
		self.Settings.setValue('HLedge', self.handlerLedgeVar)
		self.Settings.endGroup()
		self.Settings.sync()
