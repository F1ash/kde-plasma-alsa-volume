#  SensitivitySlider.py
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

from PyQt4.QtGui import QWidget, QSlider, \
                        QLabel, QVBoxLayout
from PyQt4.QtCore import Qt

class SensitivitySlider(QWidget):
	def __init__(self, obj = None, parent = None):
		QWidget.__init__(self, parent)

		if obj is None : return

		self.layout = QVBoxLayout()

		self.sensitivityLabel = QLabel()
		self.layout.addWidget(self.sensitivityLabel)
		self.sensitivitySlider = QSlider()
		self.sensitivitySlider.setRange(0, 200)
		self.sensitivitySlider.setSingleStep(1)
		self.sensitivitySlider.setOrientation(Qt.Horizontal)
		self.sensitivitySlider.valueChanged[int].connect(self.sensitivityDisplay)
		self.layout.addWidget(self.sensitivitySlider)

		self.setLayout(self.layout)
		if obj.config().hasKey("Sensitivity") :
			data_ = obj.config().readEntry("Sensitivity")
			value, state = data_.toInt()
			if not state : value = 100
		else : value = 100
		self.sensitivitySlider.setValue(value)

	def sensitivityDisplay(self, i = 100):
		if i<100 :
			s = 2 + int(float(100-i)/33)
			self.sensitivityLabel.setText('<b><u>Sensitivity of sliders</u>: 1/%s</b>' % s)
		else :
			s = 1 + int(float(i-100)/25)
			self.sensitivityLabel.setText('<b><u>Sensitivity of sliders</u>: %i</b>' % s)
