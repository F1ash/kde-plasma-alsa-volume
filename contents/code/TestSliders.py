# -*- coding: utf-8 -*-
#  TestSliders.py
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
from PyQt4.QtGui import QVBoxLayout, QHBoxLayout, \
                        QSlider, QWidget, QPushButton, \
                        QIcon
from Style import STYLE_HORYZ, STYLE_VERT

class TestSliders(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.obj = obj
		self.Parent = parent

		self.wV = QWidget(self)
		self.wH = QWidget(self)
		self.setTestWidgetsSize()

		self.testVSlider1 = QSlider()
		self.testVSlider1.setOrientation(Qt.Vertical)
		self.testVSlider2 = QSlider()
		self.testVSlider2.setOrientation(Qt.Vertical)
		self.testVSlider3 = QSlider()
		self.testVSlider3.setOrientation(Qt.Vertical)

		self.testHSlider1 = QSlider()
		self.testHSlider1.setOrientation(Qt.Horizontal)
		self.testHSlider2 = QSlider()
		self.testHSlider2.setOrientation(Qt.Horizontal)
		self.testHSlider3 = QSlider()
		self.testHSlider3.setOrientation(Qt.Horizontal)

		self.setSlidersStyleSheet()

		self.commonLayout = QHBoxLayout()
		self.commonLayout.setSpacing(0)

		self.vertLayout = QVBoxLayout()
		self.vertLayout.setAlignment(Qt.AlignCenter)
		self.vertLayout.setSpacing(0)
		self.vertLayout.setContentsMargins(0,0,0,0)
		self.vertLayout.addWidget(self.testHSlider1)
		self.vertLayout.addWidget(self.testHSlider2)
		self.vertLayout.addWidget(self.testHSlider3)
		self.wV.setLayout(self.vertLayout)
		
		self.hrznLayout = QHBoxLayout()
		self.hrznLayout.setAlignment(Qt.AlignCenter)
		self.hrznLayout.setSpacing(0)
		self.hrznLayout.setContentsMargins(0,0,0,0)
		self.hrznLayout.addWidget(self.testVSlider1)
		self.hrznLayout.addWidget(self.testVSlider2)
		self.hrznLayout.addWidget(self.testVSlider3)
		self.wH.setLayout(self.hrznLayout)

		self.clearChanges = QPushButton(QIcon().fromTheme('view-refresh'), "Clear")
		self.clearChanges.clicked.connect(self.clearSlidersChanges)

		self.commonLayout.addWidget(self.wV)
		self.commonLayout.addWidget(self.wH)
		self.commonLayout.addWidget(self.clearChanges)
		self.setLayout(self.commonLayout)

	def setSlidersSize(self, v1, v2, v3, v4, get_Style = None):
		if get_Style is None :
			styleHSheet, styleVSheet = STYLE_HORYZ, STYLE_VERT
		elif type(get_Style)==tuple :
			styleHSheet, styleVSheet = get_Style
		styleHSheet = styleHSheet.replace("__MARGIN__", v1)
		styleVSheet = styleVSheet.replace("__MARGIN__", v1)
		styleHSheet = styleHSheet.replace("__THICK__", v2)
		styleVSheet = styleVSheet.replace("__THICK__", v2)
		styleHSheet = styleHSheet.replace("__HTHICK__", v3)
		styleVSheet = styleVSheet.replace("__HTHICK__", v3)
		styleHSheet = styleHSheet.replace("__HLEDGE__", v4)
		styleVSheet = styleVSheet.replace("__HLEDGE__", v4)
		return styleHSheet, styleVSheet

	def setSlidersColor(self, v1, v2, v3, get_Style = None):
		if get_Style is None :
			styleHSheet, styleVSheet = STYLE_HORYZ, STYLE_VERT
		elif type(get_Style)==tuple :
			styleHSheet, styleVSheet = get_Style
		styleHSheet = styleHSheet.replace("#FFF777", v1)
		styleVSheet = styleVSheet.replace("#FFF777", v1)
		styleHSheet = styleHSheet.replace("#2277FF", v2)
		styleVSheet = styleVSheet.replace("#2277FF", v2)
		styleHSheet = styleHSheet.replace("#CCCCCC", v3)
		styleVSheet = styleVSheet.replace("#CCCCCC", v3)
		return styleHSheet, styleVSheet

	def _setSlidersStyleSheet(self, h, v):
		self.testHSlider1.setStyleSheet(h)
		self.testHSlider2.setStyleSheet(h)
		self.testHSlider3.setStyleSheet(h)
		self.testVSlider1.setStyleSheet(v)
		self.testVSlider2.setStyleSheet(v)
		self.testVSlider3.setStyleSheet(v)

	def setSlidersStyleSheet(self, mark = None):
		if mark is None :
			if hasattr(self.obj, 'sizeSelect') and \
				hasattr(self.obj, 'colorSelect') :
				get_Style = self.obj.sizeSelect.setSlidersSize()
				h, v = self.obj.colorSelect.setSlidersColor(get_Style)
				self._setSlidersStyleSheet(h, v)
			else :
				self._setSlidersStyleSheet(self.obj.style_horiz, self.obj.style_vert)
		elif not mark :
			get_Style = self.obj.colorSelect.setSlidersColor()
			h, v = self.obj.sizeSelect.setSlidersSize(get_Style)
			self._setSlidersStyleSheet(h, v)
			self.obj.sizeSelect.testSliders._setSlidersStyleSheet(h, v)

	def clearSlidersChanges(self):
		if self.Parent == self.obj.sizeSelect :
			self.Parent.restoreValues()
		if self.Parent == self.obj.colorSelect :
			self.Parent.restoreValues()
			self.setSlidersStyleSheet(False)
			self.Parent.restoreValues()
			self.setSlidersStyleSheet(False)

	def setTestWidgetsSize(self):
		size = self.obj.size()
		if not size.isValid() : return
		if self.Parent.Settings.value('Vertical::widgetOrientation').toString() == '1':
			parameter = size.width()
		else :
			parameter = size.height()
		self.wV.setFixedWidth(parameter)
		self.wH.setFixedHeight(parameter)
		self.Parent.updateGeometry()
