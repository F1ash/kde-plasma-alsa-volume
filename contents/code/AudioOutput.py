#  AudioOutput.py
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

from PyQt4.QtGui import QIcon, QPushButton
from PyQt4.QtCore import pyqtSlot
from PyKDE4.plasma import Plasma
import alsaaudio

class AudioOutput():
	def __init__(self, mix = 'Master', parent = None, i = 0, cardIndex = 0):

		self.Parent = parent
		self.id_ = i

		self.mix = mix
		self.cardIndex = cardIndex

		self.playIcon = QIcon().fromTheme('media-playback-start')
		self.muteIcon = QIcon().fromTheme('media-playback-stop')

		self.mixerID = None
		for _id in xrange(100) :				## how much?
			try :
				x = ''
				self.Mixer = alsaaudio.Mixer(self.mix, _id, cardindex = self.cardIndex)
			except alsaaudio.ALSAAudioError, x:
				#print x
				continue
			self.mixerID = _id
			break

		#print self.Mixer.mixer(), self.mix
		if self.mixerID is not None :
			self.capability = self.Mixer.volumecap()
			self.oldValue = self.Mixer.getvolume()
			#print self.oldValue, self.capability, self.mix
			self.Mute_ = QPushButton(self.playIcon, '')
			try :
				self.setMuteFromDevice()
			except alsaaudio.ALSAAudioError, x :
				# print x, '\n'
				self.Mute_ = None
			finally : pass
		else :
			self.capability = []

	def initSliderValues(self):
		if self.Parent.config().hasKey(self.mix) :
			data_ = self.Parent.config().readEntry(self.mix).split(',')
			volume, state = data_.takeFirst().toInt()
			if not state : volume = int(min(self.oldValue))
			m, state = data_.takeLast().toInt()
			if state and m>=0 : self.setMute(m)
		else :
			volume = int(min(self.oldValue))
		self.setALSAMixerVolume(volume)
		value = self.valueFromVolume(volume)
		#print 'Init: %s\n\t\tvolume(%s)' % (self.mix, volume)
		if hasattr(self.Parent, 'sliderHandle') :
			self.setCurrentValue(self.Parent.sliderHandle[self.id_], value, volume)
		if hasattr(self.Parent, 'sliderHPlasma') :
			if (type(self.Parent.sliderHPlasma[self.id_]) is not str) :
				self.setCurrentValue(self.Parent.sliderHPlasma[self.id_], value, volume, True)

	def setALSAMixerVolume(self, volume):
		i = 0
		for channal in self.oldValue :
			self.Mixer.setvolume(volume, i)
			i += 1

	@pyqtSlot(int, name="receiveVolumeFromDevice")
	def receiveVolumeFromDevice(self):
		vol_ = alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getvolume()
		volume = int(min(vol_))
		if volume != int(min(self.oldValue)) :
			#print "_1", self.mix, volume
			self.setValueFromDevice(volume)
		if not (self.Mute_ is None) : self.setMuteFromDevice()

	@pyqtSlot(int, name="changeMuteState")
	def changeMuteState(self):
		Mute = 0
		for i in self.Mixer.getmute():
			Mute += int(i)
		self.setMute(0 if Mute else 1)

	def setMute(self, Mute):
		if 0 == Mute:
			self.Mixer.setmute(0)
			MuteStat = 'Active'
			self.MuteStat = 0
			self.Mute_.setIcon(self.muteIcon)
		elif Mute > 0 :
			self.Mixer.setmute(1)
			MuteStat = 'Mute'
			self.MuteStat = 1
			self.Mute_.setIcon(self.playIcon)
		if Mute >= 0 : self.Mute_.setToolTip('Status: ' + MuteStat)

	def setMuteFromDevice(self):
		Mute = 0
		for i in alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getmute():
			Mute += int(i)
		self.setMute(1 if Mute else 0)

	def valueFromVolume(self, volume):
		if self.Parent.sensitivity > 1 :
				value = int(round(float(volume)/self.Parent.sensitivity))
		elif self.Parent.sensitivity < 1 :
			value = volume*abs(self.Parent.sensitivity)
		else : value = volume
		return value

	@pyqtSlot(int, name="setValueFromDevice")
	def setValueFromDevice(self, volume):
		if volume >= 100 :
			value = self.Parent.sliderMaxValue
		elif volume >= 0 :
			value = self.valueFromVolume(volume)
		else : return

		if volume != int(min(self.oldValue)) :
			self.applyParameters(value, volume)

	def volumeFromValue(self, value):
		if self.Parent.sensitivity > 1 :
			volume = value*self.Parent.sensitivity
		elif self.Parent.sensitivity < 1 :
			volume = int(round(float(value)/abs(self.Parent.sensitivity)))
		else : volume = value
		return volume

	@pyqtSlot(int, name="receiveValueFromSlider")
	def receiveValueFromSlider(self, value):
		if value >= self.Parent.sliderMaxValue :
			volume = 100
		else :
			volume = self.volumeFromValue(value)

		if volume != int(min(self.oldValue)) :
			self.setALSAMixerVolume(volume)
			#print "2", self.mix, volume
			self.applyParameters(value, volume)

	def applyParameters(self, value, volume):
		if hasattr(self.Parent, 'sliderHandle') and len(self.Parent.sliderHandle)-1 >= self.id_ :
			self.setCurrentValue(self.Parent.sliderHandle[self.id_], value, volume)
		if hasattr(self.Parent, 'sliderHPlasma') and len(self.Parent.sliderHPlasma)-1 >= self.id_ :
			if (type(self.Parent.sliderHPlasma[self.id_]) is not str) :
				self.setCurrentValue(self.Parent.sliderHPlasma[self.id_], value, volume, True)

	def setCurrentValue(self, obj, value, volume, panel = False):
		i = 0
		for channal in self.oldValue :
			self.oldValue[i] = volume
			i += 1
		#print "3", self.mix, value, "<->", volume, ":", self.oldValue[0], "PDial" if panel else "CDDial"
		obj.setValue(value)
		obj.setToolTip(obj.name + ' ' + str(int(self.oldValue[0])) + '%')
		if panel :
			InfoList = self.getInfoList()
			Plasma.ToolTipManager.self().setContent( self.Parent.applet, Plasma.ToolTipContent( \
					self.Parent.icon.toolTip(), \
					InfoList, \
					self.Parent.icon.icon() ) )

	def getInfoList(self):
		i = 0
		_list = "<table cellspacing='0' cellpadding='10' border='0' align='left' width='80%'><tbody>"
		for slider in self.Parent.sliderHandle :
			if (type(slider) is not str) :
				sliderName = slider.name
				if sliderName in self.Parent.panelDevices :
					name = sliderName
					volume = self.Parent.ao[i].oldValue[0]
					#_list += '<pre><b>' + name + '&#09;&#09;' + str(volume) + '</b></pre>'
					_list += '<tr><td><b>' + name + '</b></td><td align="right"><b>' + str(volume) + '</b></td></tr>'
			i += 1
		_list += "</tbody></table>"
		return _list

