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
			# print self.oldValue, self.capability
			try :
				Mute = 0
				for i in alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getmute() :
					Mute += int(i)
				if Mute == 0:
					MuteStat = 'Active'
					self.MuteStat = 0
					self.Mute_ = QPushButton(self.muteIcon, '')
				else:
					MuteStat = 'Mute'
					self.MuteStat = 1
					self.Mute_ = QPushButton(self.playIcon, '')
				#self.Mute_.setMaximumSize(40.0, 40.0)
				self.Mute_.setToolTip('Status: ' + MuteStat)
			except alsaaudio.ALSAAudioError, x :
				# print x, '\n'
				self.Mute_ = ''
			finally:
				pass
		else :
			self.capability = []
		if self.Parent.config().hasKey(self.mix) :
			data_ = self.Parent.config().readEntry(self.mix).split(',')
			m, state = data_.takeLast().toInt()
			if state and m>=0 : self.setMute(m)
			v, state = data_.takeFirst().toInt()
			if state and v>=0 : self.setVolume(v)
			#print 'Init: %s\n\t\tvolume(%s),\tmute(%s)' % (self.mix, v, m)

	def setVolume_timeout(self):
		vol_ = alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getvolume()
		self.setVolume(int(min(vol_)))

	def setMuted_(self):
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

	def setMuted_timeout(self):
		Mute = 0
		for i in alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getmute():
			Mute += int(i)
		if self.MuteStat != Mute : self.setMute(Mute)

	def setVolume(self, vol_):
		i = 0
		for channal in self.oldValue:
			self.oldValue[i] = vol_
			self.Mixer.setvolume(vol_, i)
			i += 1
		if hasattr(self.Parent, 'sliderHandle') and len(self.Parent.sliderHandle)-1 >= self.id_ :
			self.setCurrentValue(self.Parent.sliderHandle[self.id_])
		if hasattr(self.Parent, 'sliderHPlasma') and len(self.Parent.sliderHPlasma)-1 >= self.id_ :
			if (type(self.Parent.sliderHPlasma[self.id_]) is not str) :
				self.setCurrentValue(self.Parent.sliderHPlasma[self.id_], True)

	def setCurrentValue(self, obj, panel = False):
		vol_ = int(min(self.oldValue))
		obj.setValue(vol_)
		obj.setToolTip(obj.name + ' ' + str(vol_) + '%')
		if panel :
			InfoList = self.getInfoList()
			Plasma.ToolTipManager.self().setContent( self.Parent.applet, Plasma.ToolTipContent( \
					self.Parent.icon.toolTip(), \
					InfoList, \
					self.Parent.icon.icon() ) )

	def getInfoList(self):
		i = 0
		_list = ''
		for slider in self.Parent.sliderHandle:
			if (type(slider) is not str):
				sliderName = slider.name
				if sliderName in self.Parent.panelDevices :
					name = sliderName; value = str(slider.value())
					_list += '<pre><b>' + name + '&#09;' + value + '</b></pre>'
			i += 1
		return _list

