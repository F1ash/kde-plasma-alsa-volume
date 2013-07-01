# -*- coding: utf-8 -*-
#  main.py
#  
#  Copyright 2012 Flash <kaperang07@gmail.com>
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

try :
	global warningMsg
	warningMsg = ''
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyKDE4.kdecore import *
	from PyKDE4.kdeui import *
	from PyKDE4.plasma import Plasma
	from PyKDE4 import plasmascript
	from Style import STYLE_HORYZ, STYLE_VERT
	import os.path, string, select, time, alsaaudio
except ImportError, warningMsg :
	print "ImportError", warningMsg
finally:
	'O`key'

class T(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self)

		self.Parent = parent
		self.Key = True
		self.pollingObj = None
		self.fds = None
		self.setTerminationEnabled(True)

	def run(self):
		while self.Key :
			x = ''
			try:
				eventDevice = alsaaudio.Mixer()
				self.fds = eventDevice.polldescriptors()
				self.pollingObj = select.poll()
				self.pollingObj.register(self.fds[0][0], self.fds[0][1])
				self.pollingObj.poll()
				if self.Key : self.Parent.emit(SIGNAL('changed()'))
			except Exception, x:
				print x
			finally :
				self.closePolling()
		return

	def stop(self):
		self.Key = False
		self.closePolling()

	def closePolling(self):
		if self.fds :
			self.pollingObj.unregister(self.fds[0][0])
		del self.pollingObj
		del self.fds
		self.pollingObj = None
		self.fds = None

	def _terminate(self):
		self.stop()
		self.Parent.closeApplet.emit()

class plasmaVolume(plasmascript.Applet):
	closeApplet = pyqtSignal()
	killThread  = pyqtSignal()
	refresh     = pyqtSignal()
	refreshByDP = pyqtSignal()
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)

	def initColor(self):
		self.fontColourVar = self.initValue('fontColour')
		self.sliderColour1Var = self.initValue('sliderColour1', 1355022335)
		self.sliderColour2Var = self.initValue('sliderColour2', 1355022335)
		self.handlerColourVar = self.initValue('handlerColour', 1355022335)

		self.style_horiz = STYLE_HORYZ
		self.style_vert = STYLE_VERT
		sliderColour1 = ColorWidget(self).getRGBaStyle((QString(self.sliderColour1Var).toUInt()[0], True), 'slider')
		sliderColour2 = ColorWidget(self).getRGBaStyle((QString(self.sliderColour2Var).toUInt()[0], True), 'slider')
		handlerColour = ColorWidget(self).getRGBaStyle((QString(self.handlerColourVar).toUInt()[0], True), 'slider')
		#print sliderColour1, sliderColour2, handlerColour
		self.style_horiz = string.replace(self.style_horiz, "#FFF777", sliderColour1)
		self.style_vert = string.replace(self.style_vert, "#FFF777", sliderColour1)
		self.style_horiz = string.replace(self.style_horiz, "#2277FF", sliderColour2)
		self.style_vert = string.replace(self.style_vert, "#2277FF", sliderColour2)
		self.style_horiz = string.replace(self.style_horiz, "#CCCCCC", handlerColour)
		self.style_vert = string.replace(self.style_vert, "#CCCCCC", handlerColour)

	def initValue(self, key_, default = '0'):
		if self.Settings.contains(key_) :
			#print key_, Settings.value(key_).toString()
			return self.Settings.value(key_).toString()
		else :
			if default == '0' :
				default = ColorWidget(self).getSystemColor('int')
			self.Settings.setValue(key_, QVariant(default))
			#print key_, Settings.value(key_).toString()
			return default

	def init(self):
		self.setImmutability(Plasma.Mutable)
		#s = ''
		#for i in xrange(60) : s += '*'
		#print s
		#print 'New init in: ', time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime())
		#print [str(s) for s in self.config().keyList()], ' ALSA Devices'
		self.Flag = T(self)
		self.setHasConfigurationInterface(True)

		self.Settings = QSettings('plasmaVolume','plasmaVolume')
		self.initColor()
		self.panelDevices = self.Settings.value('PanelDevices').toString().split(',')
		self.panelDevices.removeAll('')

		self.connect(self.applet, SIGNAL('destroyed()'), self.down)
		self.closeApplet.connect(self._close)
		self.killThread.connect(self.stopWaitingVolumeChange)
		self.refresh.connect(self.refreshData)
		self.refreshByDP.connect(self.refreshByDevicePanel)

		self._icon = QIcon().fromTheme('preferences-desktop-sound')
		self.initIcon()

		self.Dialog = Plasma.Dialog()
		self.Dialog.setAspectRatioMode(Plasma.IgnoreAspectRatio)
		self.Dialog.setResizeHandleCorners( Plasma.Dialog.ResizeCorner(2) )

		self.Dialog.layout = QGridLayout()

		global warningMsg
		if warningMsg != '' :
			self.layout = QGraphicsLinearLayout()
			labelMsg = Plasma.Label()
			Msg = 'Error : ' + str(warningMsg) + '.<br>Please, install necessary packet.'
			labelMsg.setText("<font color=red><b>" + Msg + "</b></font>")
			labelMsg.setToolTip(Msg)
			self.layout.addItem(labelMsg)
			self.setLayout(self.layout)
			self.notification("<font color=red><b>" + Msg + "</b></font>")
		else:
			self.Timer = QTimer()
			self.initContent()
			self.showPanelDevices()
			if not len(self.listAllDevices) :
				self.notification("Audio devices not found.")

		self.setLayout(self.layout)

	def initIcon(self):
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setContentsMargins(1, 1, 1, 1)
		self.layout.setSpacing(0)
		self.layout.setMinimumSize(10.0, 10.0)

		self.layoutSliders = QGraphicsGridLayout()
		self.layoutSliders.setSpacing(0)

		self.icon = Plasma.IconWidget()
		self.icon.setIcon(self._icon)
		self.icon.setToolTip('ALSA Volume Control')
		self.connect(self.icon, SIGNAL('clicked()'), self.showSliders)
		self.icon.setMaximumSize(40.0, 40.0)

	def startWaitingVolumeChange(self):
		if len(self.listAllDevices) and not self.Flag.isRunning() :
			self.Flag.Key = True
			self.Flag.start()

	def stopWaitingVolumeChange(self):
		if self.Flag.isRunning() :
			self.Flag.stop()

	def initContent(self):
		self.initColor()
		if 'Dialog' in dir(self) :
			del self.Dialog
			self.Dialog = QWidget()
			self.Dialog.layout = QGridLayout()
			if 'Scroll' in dir(self) :
				del self.Scroll
			if 'ScrollWidget' in dir(self) :
				del self.ScrollWidget
			self.Scroll = QScrollArea()

			fontStyle = ColorWidget(self).getRGBaStyle((QString(self.fontColourVar).toUInt()[0], True))
			iconPath = QIcon().fromTheme('view-refresh')
			self.rescanDevices = QPushButton(iconPath, '')
			#self.rescanDevices.setStyleSheet(fontStyle)
			self.rescanDevices.setToolTip('Rescan')
			self.rescanDevices.clicked.connect(self.rescan)
			self.panelNameLabel = QLabel('<b>Common Device Panel</b>')
			self.panelNameLabel.setStyleSheet(fontStyle)
			self.Dialog.layout.addWidget(self.panelNameLabel,0,1)
			self.Dialog.layout.addWidget(self.rescanDevices,0,2)

		self.sliderHandle = []
		self.label = []
		self.ao = []
		i = 0
		self.listAllDevices = []
		cardList = alsaaudio.cards()
		cardIndexList = []
		for card in xrange(100) :
			try:
				if alsaaudio.mixers(card) :
					cardIndexList.append(card)
					#print card, alsaaudio.mixers(card), cardList[i]; i += 1
			except alsaaudio.ALSAAudioError :
				#print card, ' error'
				pass
			finally : pass
		i = 0
		for card in cardIndexList :
			try:
				for audioDevice in alsaaudio.mixers(card) :
					self.listAllDevices.append((audioDevice, card, cardList[i]))
			except alsaaudio.ALSAAudioError :
				#print card, ' error'
				pass
			finally : i += 1
		#print self.listAllDevices
		i = 0
		for audioDevice in self.listAllDevices :
			name = str(audioDevice[0])
			cardIndex = audioDevice[1]
			card = audioDevice[2]
			#print name, cardIndex, card
			self.ao.append(AudioOutput(name, self, i, cardIndex))
			if not ( self.ao[i].capability in ([], ['']) ) :

				self.sliderHandle.append(QSlider(Qt.Horizontal))
				self.sliderHandle[i].setTickPosition(2)
				self.sliderHandle[i].name = name + ' \\ ' + card
				self.ao[i].setCurrentValue(self.sliderHandle[i])
				self.Dialog.layout.addWidget(self.sliderHandle[i],i+1,5)
				self.sliderHandle[i].valueChanged.connect(self.ao[i].setVolume)

				self.label.append(name)
				self.label[i] = QLabel('<b><i>' + name + ' \\ ' + card + '</i></b>')
				self.label[i].setStyleSheet(fontStyle)
				self.label[i].setToolTip(name)
				self.Dialog.layout.addWidget(self.label[i],i+1,1)

				if (type(self.ao[i].Mute_) is not str):
					self.Dialog.layout.addWidget(self.ao[i].Mute_,i+1,2)
					self.ao[i].Mute_.clicked.connect(self.ao[i].setMuted_)
					self.connect(self, SIGNAL('changed()'), self.ao[i].setMuted_timeout)

				self.connect(self, SIGNAL('changed()'), self.ao[i].setVolume_timeout)
			else:
				self.label.append('')
				self.sliderHandle.append('')
				#print name, cardIndex, card, 'not capability'
			i += 1

		self.Dialog.setLayout(self.Dialog.layout)
		self.Scroll.setWidgetResizable(True)
		self.Scroll.setWidget(self.Dialog)
		self.ScrollWidget = Plasma.Dialog()
		self.ScrollWidget.layout = QGridLayout()
		self.ScrollWidget.layout.addWidget(self.Scroll, 0, 0)
		self.ScrollWidget.setMaximumHeight(650)
		self.ScrollWidget.setMinimumSize(350, 350)
		self.ScrollWidget.setLayout(self.ScrollWidget.layout)
		self.ScrollWidget.setAspectRatioMode(Plasma.IgnoreAspectRatio)
		self.ScrollWidget.setResizeHandleCorners( Plasma.Dialog.ResizeCorner(6) )

	def showPanelDevices(self):
		if not (self.layout is None) :
			self.layout.removeItem(self.icon)
			del self.layout
		if not (self.layoutSliders is None) :
			del self.layoutSliders
		self.initIcon()

		if self.Settings.value('Icon_On').toString() == '1'\
							or self.panelDevices.isEmpty() :
			self.layout.addItem(self.icon)
			self.icon.show()

		if self.Settings.value('Vertical::widgetOrientation').toString() == '1':
			oriental_ = Qt.Horizontal
			style_ = self.style_horiz
			if self.formFactor() == Plasma.Horizontal :
				self.setMaximumWidth(35)
			elif self.formFactor() in (Plasma.Planar, Plasma.MediaCenter) :
				pass
		else:
			oriental_ = Qt.Vertical
			style_ = self.style_vert
			if self.formFactor() == Plasma.Vertical :
				self.setMaximumHeight(35)
			elif self.formFactor() in (Plasma.Planar, Plasma.MediaCenter) :
				pass

		i = 0
		self.sliderHPlasma = []
		# print self.panelDevices, '---'
		for slider in self.sliderHandle:
			if (type(slider) is not str):
				sliderName = slider.name
				if sliderName in self.panelDevices:    ## ["Master","PCM","Front","Line"]:
					if self.ao[i].capability != [] :
						# print sliderName,'--'
						self.sliderHPlasma.append(Plasma.Slider())
						self.sliderHPlasma[i].setOrientation(oriental_)
						self.sliderHPlasma[i].setToolTip(sliderName)
						self.sliderHPlasma[i].name = sliderName
						self.sliderHPlasma[i].setStyleSheet(style_)
						self.sliderHPlasma[i].mouseDoubleClickEvent = self.mouseDoubleClickEvent
						self.sliderHPlasma[i].mouseReleaseEvent = self.mouseReleaseEvent
						self.ao[i].setCurrentValue(self.sliderHPlasma[i])
						if oriental_ == Qt.Vertical:
							self.layoutSliders.addItem(self.sliderHPlasma[i], 0, i)
						else:
							self.layoutSliders.addItem(self.sliderHPlasma[i], i, 0)
						self.sliderHPlasma[i].valueChanged.connect(self.ao[i].setVolume)
					else:
						self.sliderHPlasma.append('')
				else:
					self.sliderHPlasma.append('')
			else:
				self.sliderHPlasma.append('')
			i += 1

		self.layout.addItem(self.layoutSliders)
		self.setLayout(self.layout)
		self.Timer.singleShot(2000, self.startWaitingVolumeChange)

	def showSliders(self):
		if self.ScrollWidget.isVisible():
			self.ScrollWidget.close()
			self.writeParameters()
		else:
			self.ScrollWidget.show()
			self.ScrollWidget.move(self.popupPosition(self.ScrollWidget.sizeHint()))   ##Dialog

	def createConfigurationInterface(self, parent):
		self.colorSelect = ColorWidget(self, parent)
		parent.addPage(self.colorSelect, "Color")
		self.selectDevice = DevicePanel(self, parent)
		parent.addPage(self.selectDevice,"Panel Devices")
		self.interfaceSettings = InterfaceSettings(self, parent)
		parent.addPage(self.interfaceSettings, 'Interface')
		self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
		self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

	def showConfigurationInterface(self):
		dialog = KPageDialog()
		dialog.setModal(True)
		dialog.setFaceType(KPageDialog.List)
		dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
		self.createConfigurationInterface(dialog)
		dialog.exec_()
		dialog.move(self.popupPosition(dialog.sizeHint()))

	def rescan(self):
		self.ScrollWidget.close()
		self.initContent()
		self.showPanelDevices()
		self.showSliders()
		if not len(self.listAllDevices) :
			self.notification("Audio devices not found.")

	def refreshByDevicePanel(self):
		self.initContent()
		self.showPanelDevices()
		self.showConfigurationInterface()
		if not len(self.listAllDevices) :
			self.notification("Audio devices not found.")

	def refreshData(self):
		self.Settings.sync()
		self.initContent()
		self.showPanelDevices()

	def configAccepted(self):
		self.stopWaitingVolumeChange()
		self.selectDevice.refreshPanelDevices(self)
		self.interfaceSettings.refreshInterfaceSettings()
		self.colorSelect.refreshInterfaceSettings()
		self.refresh.emit()

	def configDenied(self):
		pass

	def writeParameters(self):
		if 'listAllDevices' in dir(self) :
			for i in xrange(len(self.listAllDevices)) :
				try :
					if self.ao[i].capability != [] :
						muteStat = self.ao[i].MuteStat if hasattr(self.ao[i], 'MuteStat') else -1
						s = (self.ao[i].mix, self.ao[i].capability, self.ao[i].oldValue, muteStat)
						#print '\t%s\t%s\n\t%s\t%s' % s
						data = QStringList() << str(self.ao[i].oldValue[0]) << str(muteStat)
						self.config().writeEntry(self.ao[i].mix, data)
				except Exception, x :
					#print x
					pass
				finally : pass
		self.config().sync()
		self.notification('Parameters are saved.')

	def notification(self, msg):
		newMailNotify = KNotification.event(KNotification.Notification, \
						QString('<b>ALSA Volume Control</b>'), \
						QString(msg), \
						self._icon.pixmap(QSize(64, 64)), \
						None, \
						KNotification.CloseOnTimeout)
		newMailNotify.sendEvent()

	def down(self):
		self.disconnect(self.applet, SIGNAL('destroyed()'), self.down)
		x = ''
		if 'listAllDevices' in dir(self) :
			for i in xrange(len(self.listAllDevices)) :
				try :
					if self.ao[i].capability != [] :
						self.disconnect(self, SIGNAL('changed()'), self.ao[i].setMuted_timeout)
						self.disconnect(self, SIGNAL('changed()'), self.ao[i].setVolume_timeout)
				except Exception, x :
					#print x
					pass
				finally : pass
		if self.Flag.isRunning() : self.Flag._terminate()
		else : self._close()

	def mouseDoubleClickEvent(self, ev):
		self.showConfigurationInterface()

	def mousePressEvent(self, ev):
		if ev.type() == QEvent.GraphicsSceneMousePress :
			ev.accept()
	def mouseReleaseEvent(self, ev):
		if ev.type() == QEvent.GraphicsSceneMouseRelease :
			#ev.ignore()
			self.refreshData()

	def _close(self):
		print "plasmaVolume destroyed manually."

	def __del__(self): self.down()

class AudioOutput():
	def __init__(self, mix = 'Master', parent = None, i = 0, cardIndex = 0):

		self.Parent = parent
		self.id_ = i

		self.mix = mix
		self.cardIndex = cardIndex

		self.playIcon = QIcon().fromTheme('kt-start')
		self.muteIcon = QIcon().fromTheme('kt-stop')

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
		listPanelDevices = string.split(str(str_raw),',')
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

class ColorWidget(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = obj.Settings

		self.colourIcon = QIcon().fromTheme('color')

		self.fontColourVar = self.initValue('fontColour')
		self.sliderColour1Var = self.initValue('sliderColour1', 1355022335)
		self.sliderColour2Var = self.initValue('sliderColour2', 1355022335)
		self.handlerColourVar = self.initValue('handlerColour', 1355022335)

		self.layout = QGridLayout()

		self.fontColourLabel = QLabel('fontColour :')
		self.fontColourLabel.setStyleSheet(self.getRGBaStyle((QString(self.fontColourVar).toUInt()[0], True)))
		self.layout.addWidget(self.fontColourLabel, 0, 0)
		self.fontColourButton = QPushButton(self.colourIcon, '')
		self.fontColourButton.setMaximumWidth(30)
		self.fontColourButton.setToolTip('Slider Shield Font Color')
		self.connect(self.fontColourButton, SIGNAL('clicked()'), self.fontColour)
		self.layout.addWidget(self.fontColourButton, 0, 1)

		self.sliderColour1Label = QLabel('sliderColour1 :')
		self.sliderColour1Label.setStyleSheet(self.getRGBaStyle((QString(self.sliderColour1Var).toUInt()[0], True)))
		self.layout.addWidget(self.sliderColour1Label, 1, 0)
		self.sliderColour1Button = QPushButton(self.colourIcon, '')
		self.sliderColour1Button.setMaximumWidth(30)
		self.sliderColour1Button.setToolTip('Background Slider Color')
		self.connect(self.sliderColour1Button, SIGNAL('clicked()'), self.sliderColour1)
		self.layout.addWidget(self.sliderColour1Button, 1, 1)

		self.sliderColour2Label = QLabel('sliderColour2 :')
		self.sliderColour2Label.setStyleSheet(self.getRGBaStyle((QString(self.sliderColour2Var).toUInt()[0], True)))
		self.layout.addWidget(self.sliderColour2Label, 2, 0)
		self.sliderColour2Button = QPushButton(self.colourIcon, '')
		self.sliderColour2Button.setMaximumWidth(30)
		self.sliderColour2Button.setToolTip('Slider Color')
		self.connect(self.sliderColour2Button, SIGNAL('clicked()'), self.sliderColour2)
		self.layout.addWidget(self.sliderColour2Button, 2, 1)

		self.handlerColourLabel = QLabel('handlerColour :')
		self.handlerColourLabel.setStyleSheet(self.getRGBaStyle((QString(self.handlerColourVar).toUInt()[0], True)))
		self.layout.addWidget(self.handlerColourLabel, 3, 0)
		self.handlerColourButton = QPushButton(self.colourIcon, '')
		self.handlerColourButton.setMaximumWidth(30)
		self.handlerColourButton.setToolTip('handler Color')
		self.connect(self.handlerColourButton, SIGNAL('clicked()'), self.handlerColour)
		self.layout.addWidget(self.handlerColourButton, 3, 1)

		self.setLayout(self.layout)

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

	def sliderColour2(self):
		colour, yes, style = self.getColour(QString(self.sliderColour2Var).toUInt())
		if yes :
			self.sliderColour2Var = colour
			self.sliderColour2Label.clear()
			self.sliderColour2Label.setStyleSheet(style)
			self.sliderColour2Label.setText('sliderColour2 :')

	def handlerColour(self):
		colour, yes, style = self.getColour(QString(self.handlerColourVar).toUInt())
		if yes :
			self.handlerColourVar = colour
			self.handlerColourLabel.clear()
			self.handlerColourLabel.setStyleSheet(style)
			self.handlerColourLabel.setText('handlerColour :')

	def refreshInterfaceSettings(self):
		self.Settings.setValue('fontColour', self.fontColourVar)
		self.Settings.setValue('sliderColour1', self.sliderColour1Var)
		self.Settings.setValue('sliderColour2', self.sliderColour2Var)
		self.Settings.setValue('handlerColour', self.handlerColourVar)
		self.Settings.sync()

def CreateApplet(parent):
	return plasmaVolume(parent)
