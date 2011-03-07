# -*- coding: utf-8 -*-
try :
	global warningMsg
	warningMsg = ''
	from PyKDE4.phonon import *
	from PyQt4.QtCore import *
	from PyQt4.QtGui import *
	from PyKDE4.kdecore import *
	from PyKDE4.kdeui import *
	from PyKDE4.plasma import Plasma
	from PyKDE4 import plasmascript
	import os, alsaaudio, os.path, string, select, time
except ImportError, warningMsg :
	print "ImportError", warningMsg
finally:
	'O`key'

class T(QThread):
	def __init__(self, parent = None):
		QThread.__init__(self)

		self.Parent = parent
		self.setTerminationEnabled(True)

	def run(self):
		while True :
			x = ''
			try:
				eventDevice = alsaaudio.Mixer()
				fds = eventDevice.polldescriptors()
				pollingObj = select.poll()
				pollingObj.register(fds[0][0],fds[0][1])
				pollingObj.poll()
				# QApplication.postEvent(self.Parent, QEvent(QEvent.User))
				# print str(QEvent(QEvent.User).type())
				self.Parent.emit(SIGNAL('changed()'))
			except ALSAAudioError, x:
				print x
			except select.error, x:
				print x
			except Exception, x:
				print x
			except x :
				print x
			finally :
				pass

		return

class plasmaVolume(plasmascript.Applet):
	def __init__(self,parent,args=None):
		plasmascript.Applet.__init__(self,parent)

	def initColor(self):
		self.fontColourVar = self.initValue('fontColour')
		self.sliderColour1Var = self.initValue('sliderColour1')
		self.sliderColour2Var = self.initValue('sliderColour2')
		self.handlerColourVar = self.initValue('handlerColour')

		kdehome = unicode(KGlobal.dirs().localkdedir())
		# print kdehome

		f = open(kdehome + "share/apps/plasma/plasmoids/plasmaVolume/contents/style/style_horiz.css")
		self.style_horiz = f.read(); f.close()
		f = open(kdehome + "share/apps/plasma/plasmoids/plasmaVolume/contents/style/style_vert.css")
		self.style_vert = f.read(); f.close()
		sliderColour1 = ColorWidget().getRGBaStyle((QString(self.sliderColour1Var).toUInt()[0], True), 'slider')
		sliderColour2 = ColorWidget().getRGBaStyle((QString(self.sliderColour2Var).toUInt()[0], True), 'slider')
		handlerColour = ColorWidget().getRGBaStyle((QString(self.handlerColourVar).toUInt()[0], True), 'slider')
		#print sliderColour1, sliderColour2, handlerColour
		self.style_horiz = string.replace(self.style_horiz, "#FFF777", sliderColour1)
		self.style_vert = string.replace(self.style_vert, "#FFF777", sliderColour1)
		self.style_horiz = string.replace(self.style_horiz, "#2277FF", sliderColour2)
		self.style_vert = string.replace(self.style_vert, "#2277FF", sliderColour2)
		self.style_horiz = string.replace(self.style_horiz, "#CCCCCC", handlerColour)
		self.style_vert = string.replace(self.style_vert, "#CCCCCC", handlerColour)

	def initValue(self, key_, default = '0'):
		global Settings
		if self.Settings.contains(key_) :
			#print key_, Settings.value(key_).toString()
			return self.Settings.value(key_).toString()
		else :
			if default == '0' :
				default = ColorWidget().getSystemColor('int')
			self.Settings.setValue(key_, QVariant(default))
			#print key_, Settings.value(key_).toString()
			return default

	def init(self):
		global Flag
		Flag = T(self)
		self.setHasConfigurationInterface(True)

		self.Settings = QSettings('plasmaVolume','plasmaVolume')
		self.initColor()
		self.panelDevices = string.split(str((self.Settings.value('PanelDevices')).toString()),',')

		self.connect(self.applet, SIGNAL('destroyed()'), self.eventClose)
		self.connect(self, SIGNAL('destroyed()'), self.eventClose)
		self.connect(self, SIGNAL('killThread()'), self.stopWaitingVolumeChange)
		self.connect(self, SIGNAL('refresh()'), self.refresh)
		self.connect(self, SIGNAL('refreshByDP()'), self.refreshByDevicePanel)

		kdehome = unicode(KGlobal.dirs().localkdedir())

		path_1 = kdehome + "share/apps/plasma/plasmoids/plasmaVolume/contents/icons/sound.png"
		path_ = os.path.expanduser(path_1)
		path_2 = '/usr/share/icons/sound_pV.png'
		# print path_
		if os.path.exists(path_):
			self.path_ = path_
		else:
			self.path_ = path_2
		self.initIcon()

		self.Dialog = Plasma.Dialog()
		self.Dialog.setAspectRatioMode(Plasma.IgnoreAspectRatio)
		self.Dialog.setResizeHandleCorners( Plasma.Dialog.ResizeCorner(2) )

		self.Dialog.layout = QGridLayout()

		global warningMsg
		if warningMsg != '' :
			labelMsg = QLabel()
			Msg = 'Error : ' + str(warningMsg) + '\nPlease, install necessary packet.'
			labelMsg.setText("<font color=red><b>" + Msg + "</b></font>")
			labelMsg.setToolTip(Msg)
			self.Dialog.layout.addWidget(labelMsg,0,0)
			self.Dialog.setLayout(self.Dialog.layout)
		else:
			#self.Timer = QTimer()
			self.Mutex = QMutex()
			self.initContent()
			self.showPanelDevices()

		self.setLayout(self.layout)

	def initIcon(self):
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setContentsMargins(1, 1, 1, 1)
		self.layout.setSpacing(0)
		self.layout.setMinimumSize(10.0, 10.0)

		self.layoutSliders = QGraphicsGridLayout()
		self.layoutSliders.setSpacing(0)

		self.icon = Plasma.IconWidget()
		self.icon.setIcon(self.path_)
		self.icon.setToolTip('ALSA Volume Control')
		self.connect(self.icon, SIGNAL('clicked()'), self.showSliders)
		self.icon.setMaximumSize(40.0, 40.0)

		#self.setMinimumSize(20.0, 20.0)

	def startWaitingVolumeChange(self):
		global Flag
		if not Flag.isRunning() :
			Flag.start()

	def stopWaitingVolumeChange(self):
		global Flag
		Flag.terminate()
		while not Flag.wait() :
			Flag.quit()
			time.sleep(0.5)

	def initContent(self):
		self.initColor()
		if 'Dialog' in dir(self) :
			del self.Dialog
			self.Dialog = QWidget()
			self.Dialog.layout = QGridLayout()
			if 'Scroll' in dir(self) :
				del self.Scroll
				del self.ScrollWidget
			self.Scroll = QScrollArea()

			fontStyle = ColorWidget().getRGBaStyle((QString(self.fontColourVar).toUInt()[0], True))
			self.rescanDevices = QPushButton()
			self.rescanDevices.setStyleSheet(fontStyle)
			self.rescanDevices.setText('Rescan')
			self.rescanDevices.clicked.connect(self.rescan)
			self.panelNameLabel = QLabel('<b>Common Device Panel</b>')
			self.panelNameLabel.setStyleSheet(fontStyle)
			self.Dialog.layout.addWidget(self.panelNameLabel,0,1)
			self.Dialog.layout.addWidget(self.rescanDevices,0,5)

		global Flag
		self.sliderHandle = []
		self.label = []
		self.ao = []
		i = 0
		listAllDevices = []
		cardList = alsaaudio.cards()
		cardIndexList = []
		for card in xrange(100) :
			try:
				if alsaaudio.mixers(card) :
					cardIndexList += [card]
					#print card, alsaaudio.mixers(card), cardList[i]; i += 1
			except alsaaudio.ALSAAudioError :
				#print card, ' error'
				continue
		i = 0
		for card in cardIndexList :
			for audioDevice in alsaaudio.mixers(card) :
				listAllDevices += [ (audioDevice, card, cardList[i]) ]
			i += 1
		#print listAllDevices
		i = 0
		for audioDevice in listAllDevices :
			name = str(audioDevice[0])
			cardIndex = audioDevice[1]
			card = audioDevice[2]
			#print name, cardIndex, card
			self.ao += [name]
			self.ao[i] = AudioOutput(name, self, i, cardIndex)
			if not ( self.ao[i].capability in [ [], [''] ] ) :

				self.sliderHandle += [name]
				self.sliderHandle[i] = QSlider(Qt.Horizontal)
				self.sliderHandle[i].setTickPosition(2)
				self.sliderHandle[i].name = name + ' \\ ' + card
				self.ao[i].setCurrentValue(self.sliderHandle[i])
				self.Dialog.layout.addWidget(self.sliderHandle[i],i+1,5)
				self.sliderHandle[i].valueChanged.connect(self.ao[i].setVolume)

				self.label += [name]
				self.label[i] = QLabel('<b><i>' + name + ' \\ ' + card + '</i></b>')
				self.label[i].setStyleSheet(fontStyle)
				self.label[i].setToolTip(name)
				self.Dialog.layout.addWidget(self.label[i],i+1,1)

				if (type(self.ao[i].Mute_) is not str):
					self.Dialog.layout.addWidget(self.ao[i].Mute_,i+1,2)
					self.ao[i].Mute_.clicked.connect(self.ao[i].setMuted_)
					self.connect(self, SIGNAL('changed()'), self.ao[i].setMuted_timeout)

				self.Mutex.lock()
				self.connect(self, SIGNAL('changed()'), self.ao[i].setVolume_timeout)
				self.Mutex.unlock()
			else:
				self.label += ['']
				self.sliderHandle += ['']
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

		if str(self.Settings.value('Icon_On').toString()) == '1'\
							or ( self.panelDevices in [[],['']] ) :
			self.layout.addItem(self.icon)
			self.icon.show()
			# iconPresent = 20
		else:
			#self.layout.removeItem(self.icon)
			#self.icon.close()
			#del self.icon
			# iconPresent = 0
			pass

		# str_raw = (self.Settings.value('PanelDevices')).toString()
		# countPanelDevices = len(string.split(str(str_raw),','))

		if str(self.Settings.value('Vertical::widgetOrientation').toString()) == '1':
			oriental_ = Qt.Horizontal
			style_ = self.style_horiz
			#self.layout.setOrientation(Qt.Vertical)   !!!!!! uncomment !!!!!
			# if str(self.Settings.value('Vertical::panelOrientation').toString()) == '0':
			if self.formFactor() == Plasma.Horizontal :
				self.setMaximumWidth(35)
			elif self.formFactor() in [Plasma.Planar, Plasma.MediaCenter] :
				#self.resize(35,35)
				#self.setMaximumSize(100.0,100.0)
				pass
		else:
			oriental_ = Qt.Vertical
			style_ = self.style_vert
			#self.layout.setOrientation(Qt.Horizontal)         !!!!!! uncomment !!!!!
			# if str(self.Settings.value('Vertical::panelOrientation').toString()) == '1':
			if self.formFactor() == Plasma.Vertical :
				self.setMaximumHeight(35)
			elif self.formFactor() in [Plasma.Planar, Plasma.MediaCenter] :
				#self.resize(35,35)
				#self.setMaximumSize(100.0,100.0)
				pass

		# self.setMaximumSize(currentSize)

		i = 0
		self.sliderHPlasma = []
		# print self.panelDevices, '---'
		for slider in self.sliderHandle:
			if (type(slider) is not str):
				sliderName = slider.name
				if sliderName in self.panelDevices:    ## ["Master","PCM","Front","Line"]:
					if self.ao[i].capability != [] :
						# print sliderName,'--'
						self.sliderHPlasma += [sliderName]
						self.sliderHPlasma[i] = Plasma.Slider()
						self.sliderHPlasma[i].setOrientation(oriental_)
						self.sliderHPlasma[i].setToolTip(sliderName)
						self.sliderHPlasma[i].name = sliderName
						self.sliderHPlasma[i].setStyleSheet(style_)
						self.ao[i].setCurrentValue(self.sliderHPlasma[i])
						if oriental_ == Qt.Vertical:
							self.layoutSliders.addItem(self.sliderHPlasma[i], 0, i)
						else:
							self.layoutSliders.addItem(self.sliderHPlasma[i], i, 0)
						self.sliderHPlasma[i].valueChanged.connect(self.ao[i].setVolume)
					else:
						self.sliderHPlasma += ['']
				else:
					self.sliderHPlasma += ['']
			else:
				self.sliderHPlasma += ['']
			i += 1

		self.layout.addItem(self.layoutSliders)

		self.setLayout(self.layout)

		#self.Timer.singleShot(2000, self.startWaitingVolumeChange)
		QApplication.postEvent(self, QEvent(QEvent.User))

	def customEvent(self, event):
		if event.type() == QEvent.User :
			self.startWaitingVolumeChange()
		pass

	def showSliders(self):
		if self.ScrollWidget.isVisible():
			self.ScrollWidget.close()
		else:
			self.ScrollWidget.move(self.popupPosition(self.ScrollWidget.sizeHint()))   ##Dialog
			self.ScrollWidget.show()

	def createConfigurationInterface(self, parent):
		#self.fontSelect = FontWidget()
		# p = parent.addPage(self.fontSelect, "Font")
		self.colorSelect = ColorWidget(parent)
		parent.addPage(self.colorSelect, "Color")
		self.selectDevice = DevicePanel(self, parent)
		parent.addPage(self.selectDevice,"Panel Devices")
		self.interfaceSettings = InterfaceSettings(parent)
		parent.addPage(self.interfaceSettings, 'Interface')
		self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
		self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

	def showConfigurationInterface(self):
		dialog = KPageDialog()
		dialog.setModal(True)
		dialog.setFaceType(KPageDialog.List)
		dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
		self.createConfigurationInterface(dialog)
		dialog.move(self.popupPosition(dialog.sizeHint()))
		dialog.exec_()

	def rescan(self):
		self.ScrollWidget.close()
		self.initContent()
		self.showPanelDevices()
		self.showSliders()

	def refreshByDevicePanel(self):
		self.initContent()
		self.showPanelDevices()
		self.showConfigurationInterface()

	def refresh(self):
		self.Mutex.lock()
		self.Settings.sync()
		self.Mutex.unlock()
		self.initContent()
		self.showPanelDevices()

	def configAccepted(self):
		self.emit(SIGNAL('killThread()'))
		self.selectDevice.refreshPanelDevices(self)
		self.interfaceSettings.refreshInterfaceSettings()
		self.colorSelect.refreshInterfaceSettings()
		self.emit(SIGNAL('refresh()'))

	def configDenied(self):
		pass

	def eventClose(self):
		global Flag
		i = 0
		x = ''
		for audioDevice in alsaaudio.mixers():
			try :
				#print audioDevice
				self.disconnect(self, SIGNAL('changed()'), self.ao[i].setMuted_timeout)
				self.disconnect(self, SIGNAL('changed()'), self.ao[i].setVolume_timeout)
			except TypeError, x:
				#print x
				pass
			except x :
				#print x
				pass
			finally :
				pass
			i += 1
		self.emit(SIGNAL('killThread()'))
		self.Mutex.unlock()
		print "plasmaVolume destroyed manually."
		#self.close()

	def mouseDoubleClickEvent(self, ev):
		self.showConfigurationInterface()

class AudioOutput():
	def __init__(self, mix = 'Master', parent = None, i = 0, cardIndex = 0):

		self.Parent = parent
		self.id_ = i

		self.mix = mix
		self.cardIndex = cardIndex

		self.mixerID = None
		for _id in xrange(100) :				## how much?
			try :
				x = ''
				self.Mixer = alsaaudio.Mixer(self.mix, _id, cardindex = self.cardIndex)
			except alsaaudio.ALSAAudioError, x:
				print x
				continue
			self.mixerID = _id
			break

		# print self.Mixer.mixer()
		if self.mixerID is not None :
			self.capability = self.Mixer.volumecap()
			self.oldValue = self.Mixer.getvolume()
			# print self.oldValue, self.capability
			try :
				self.Mixer.getmute()
				self.Mute_ = QPushButton()
				self.Mute_.setText('Mute')
				Mute = 0
				for i in alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getmute() :
					Mute += int(i)
				if Mute == 0:
					MuteStat = 'Active'
					self.MuteStat = 0
				else:
					MuteStat = 'Mute'
					self.MuteStat = 1
				self.Mute_.setToolTip('Status: ' + MuteStat)
			except alsaaudio.ALSAAudioError, x :
				# print x, '\n'
				self.Mute_ = ''
			finally:
				pass
		else :
			self.capability = []

	def setVolume_timeout(self):
		vol_ = alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getvolume()
		self.setVolume(int(min(vol_)))

	def setMuted_(self):
		Mute = 0
		for i in self.Mixer.getmute():
			Mute += int(i)
		if 0 < Mute:
			self.Mixer.setmute(0)
			MuteStat = 'Active'
			self.MuteStat = 0
		else:
			self.Mixer.setmute(1)
			MuteStat = 'Mute'
			self.MuteStat = 1
		self.Mute_.setToolTip('Status: ' + MuteStat)

	def setMuted_timeout(self):
		Mute = 0
		for i in alsaaudio.Mixer(self.mix, self.mixerID, cardindex = self.cardIndex).getmute():
			Mute += int(i)
		if self.MuteStat != Mute:
			if Mute == 0:
				self.Mixer.setmute(0)
				MuteStat = 'Active'
				self.MuteStat = 0
			else:
				self.Mixer.setmute(1)
				MuteStat = 'Mute'
				self.MuteStat = 1
			self.Mute_.setToolTip('Status: ' + MuteStat)

	def setVolume(self, vol_):
		i = 0
		for channal in self.oldValue:
			self.oldValue[i] = vol_
			self.Mixer.setvolume(vol_, i)
			i += 1
		self.setCurrentValue(self.Parent.sliderHandle[self.id_])
		if (type(self.Parent.sliderHPlasma[self.id_]) is not str):
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

		self.Settings = QSettings('plasmaVolume','plasmaVolume')
		kdehome = unicode(KGlobal.dirs().localkdedir())

		self.refreshIconPath = kdehome + 'share/apps/plasma/plasmoids/plasmaVolume/contents/icons/refresh.png'
		self.refreshIcon = QIcon(self.refreshIconPath)

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
		self.Applet.emit(SIGNAL('refreshByDP()'))

	def refreshPanelDevices(self, obj):
		obj.panelDevices = []
		for item_ in self.presentDevices:
			if item_.isChecked() :
				obj.panelDevices += [item_.name]

		str_ = string.join(obj.panelDevices, ',')
		self.Settings.setValue('PanelDevices',str_)
		self.Settings.sync()

class InterfaceSettings(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = QSettings('plasmaVolume','plasmaVolume')

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
			if item_.isChecked() :
				self.Settings.setValue(item_.name, '1')
			else:
				self.Settings.setValue(item_.name, '0')

		self.Settings.sync()

class ColorWidget(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.Settings = QSettings('plasmaVolume','plasmaVolume')
		kdehome = unicode(KGlobal.dirs().localkdedir())

		self.colourIconPath = kdehome + 'share/apps/plasma/plasmoids/plasmaVolume/contents/icons/color.png'
		self.colourIcon = QIcon(self.colourIconPath)

		self.fontColourVar = self.initValue('fontColour')
		self.sliderColour1Var = self.initValue('sliderColour1')
		self.sliderColour2Var = self.initValue('sliderColour2')
		self.handlerColourVar = self.initValue('handlerColour')

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
		global Settings
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

try :
	def CreateApplet(parent):
		return plasmaVolume(parent)

	x = ''
	Flag = T()
except x :
	print x
finally :
	pass
