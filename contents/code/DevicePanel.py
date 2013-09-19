#  DevicePanel.py
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

from PyQt4.QtGui import QWidget, QIcon, \
                        QPushButton, QGridLayout, \
                        QCheckBox

class DevicePanel(QWidget):
	def __init__(self, obj = None, parent = None):
		QWidget.__init__(self, parent)

		self.Parent = parent
		self.Applet = obj

		self.Settings = obj.Settings

		self.refreshIcon = QIcon().fromTheme('view-refresh')

		self.layout = QGridLayout()

		i = 0
		self.rescanButton = QPushButton(self.refreshIcon, '')
		self.rescanButton.setToolTip('Rescan')
		self.rescanButton.clicked.connect(self.rescan)
		self.layout.addWidget(self.rescanButton, i, 1); i = + 1
		str_raw = (self.Settings.value('PanelDevices')).toString()
		self.presentDevices = []
		listPanelDevices = str(str_raw).split(',')
		for item_ in obj.sliderHandle:
			if (type(item_) is not str) :
				str_ = item_.name
				self.presentDevices += [str_]
				self.presentDevices[i - 1] = QCheckBox(str_)
				self.presentDevices[i - 1].name = str_
				if str_ in listPanelDevices:
					self.presentDevices[i - 1].setCheckState(2)
				self.layout.addWidget(self.presentDevices[i - 1], i, 0)
				i += 1

		self.setLayout(self.layout)

	def rescan(self):
		self.Parent.done(0)
		self.Applet.refreshByDP.emit()

	def refreshPanelDevices(self, obj):
		obj.panelDevices.clear()
		for item_ in self.presentDevices:
			if item_.isChecked() :
				obj.panelDevices.append(item_.name)

		self.Settings.setValue('PanelDevices', obj.panelDevices.join(','))
		self.Settings.sync()
