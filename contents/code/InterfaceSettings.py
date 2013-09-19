#  InterfaceSettings.py
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

from PyQt4.QtGui import *

class InterfaceSettings(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = obj.Settings

		self.layout = QGridLayout()

		i = 0
		self.list_ = []
		for item_ in ['Icon_On', 'Vertical::widgetOrientation']:
		# 'Vertical::panelOrientation',\
			str_ = str((self.Settings.value(item_)).toString())
			self.list_ += [item_]
			self.list_[i] = QCheckBox(item_)
			self.list_[i].name = item_
			if str_ == '1':
				self.list_[i].setCheckState(2)
			self.layout.addWidget(self.list_[i], i, 0)
			i += 1

		labelDefaultInfo = QLabel()
		labelDefaultInfo.setText('<font color=red><b>Default:<br>Horizontal::widgetOrientation</b></font>')
		self.layout.addWidget(labelDefaultInfo,i,0)

		self.setLayout(self.layout)

	def refreshInterfaceSettings(self):
		for item_ in self.list_:
			value = '1' if item_.isChecked() else '0'
			self.Settings.setValue(item_.name, value)

		self.Settings.sync()
