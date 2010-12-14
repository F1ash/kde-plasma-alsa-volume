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
	import os, alsaaudio, os.path, string, select, threading, time, sys
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

	def init(self):
		self.setHasConfigurationInterface(True)

		self.Settings = QSettings('plasmaVolume','plasmaVolume')
		self.panelDevices = string.split(str((self.Settings.value('PanelDevices')).toString()),',')

		self.connect(self.applet, SIGNAL('destroyed()'), self.eventClose)
		self.connect(self, SIGNAL('destroyed()'), self.eventClose)
		self.connect(self, SIGNAL('killThread()'), self.stopWaitingVolumeChange)

		kdehome = unicode(KGlobal.dirs().localkdedir())
		# print kdehome

		self.style_horiz = open(\
				kdehome +\
				"share/apps/plasma/plasmoids/plasmaVolume/contents/style/style_horiz.css"\
								).read()
		self.style_vert = open(\
				kdehome +\
				"share/apps/plasma/plasmoids/plasmaVolume/contents/style/style_vert.css"\
								).read()

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
		self.Dialog.resizeCorners()
		self.Dialog.setResizeHandleCorners( Plasma.Dialog.ResizeCorner(2) )
		# self.Dialog.setGeometry(580,320,640,300)

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
			self.showContent()
			self.showPanelDevices()

		self.setLayout(self.layout)

	def initIcon(self):
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setContentsMargins(1, 1, 1, 1)
		self.layout.setSpacing(0)
		self.layout.setMinimumSize(10, 10)

		self.layoutSliders = QGraphicsGridLayout()
		self.layoutSliders.setSpacing(0)

		self.icon = Plasma.IconWidget()
		self.icon.setIcon(self.path_)
		self.icon.setToolTip('SuperSimpleMixer')
		self.connect(self.icon, SIGNAL('clicked()'), self.showSliders)
		self.icon.setMaximumSize(40.0,40.0)

	def startWaitingVolumeChange(self):
		global Flag
		if not Flag.isRunning() :
			Flag = T(self)
			Flag.start()
			# print 'waiting start'

	def stopWaitingVolumeChange(self):
		global Flag
		Flag.terminate()
		while Flag.isRunning() :
			Flag.quit()
			time.sleep(0.05)
		# print 'waiting stop'

	def showContent(self):
		global Flag
		self.sliderHandle = []
		self.label = []
		self.ao = []
		i = 0
		for audioDevice in alsaaudio.mixers():
			name = str(audioDevice)
			self.ao += [name]
			self.ao[i] = AudioOutput(name, self, i)
			# print name, 'Ok'
			if not ( self.ao[i].capability in [ [], [''] ] ) :

				self.sliderHandle += [name]
				self.sliderHandle[i] = QSlider(Qt.Horizontal)
				self.sliderHandle[i].setTickPosition(2)
				self.sliderHandle[i].name = name
				self.ao[i].setCurrentValue(self.sliderHandle[i])
				self.Dialog.layout.addWidget(self.sliderHandle[i],i,5)
				self.sliderHandle[i].valueChanged.connect(self.ao[i].setVolume)

				self.label += [name]
				self.label[i] = QLabel("<font color=lime><b>" + name + "</b></font>")
				self.label[i].setToolTip(name)
				self.Dialog.layout.addWidget(self.label[i],i,1)

				if (type(self.ao[i].Mute_) is not str):
					self.Dialog.layout.addWidget(self.ao[i].Mute_,i,2)
					self.ao[i].Mute_.clicked.connect(self.ao[i].setMuted_)
					self.connect(self, SIGNAL('changed()'), self.ao[i].setMuted_timeout)

				self.Mutex.lock()
				self.connect(self, SIGNAL('changed()'), self.ao[i].setVolume_timeout)
				self.Mutex.unlock()
			else:
				self.label += ['']
				self.sliderHandle += ['']
			i += 1

		self.Dialog.setLayout(self.Dialog.layout)

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
			self.layout.setOrientation(Qt.Vertical)
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
			self.layout.setOrientation(Qt.Horizontal)
			# if str(self.Settings.value('Vertical::panelOrientation').toString()) == '1':
			if self.formFactor() == Plasma.Vertical :
				self.setMaximumHeight(35)
			elif self.formFactor() in [Plasma.Planar, Plasma.MediaCenter] :
				#self.resize(35,35)
				self.setMaximumSize(100.0,100.0)

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
		if self.Dialog.isVisible():
			self.Dialog.hide()
		else:
			self.Dialog.show()
			self.Dialog.move(self.popupPosition(self.Dialog.sizeHint()))

	def createConfigurationInterface(self, parent):
		self.fontSelect = FontWidget()
		# p = parent.addPage(self.fontSelect, "Font")
		self.colorSelect = ColorWidget()
		# parent.addPage(self.colorSelect, "Color")
		self.selectDevice = DevicePanel(self)
		parent.addPage(self.selectDevice,"Panel Devices")
		self.interfaceSettings = InterfaceSettings(self)
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

	def configAccepted(self):
		self.emit(SIGNAL('killThread()'))
		self.selectDevice.refreshPanelDevices(self)
		self.interfaceSettings.refreshInterfaceSettings(self)
		self.showPanelDevices()

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

class AudioOutput():
	def __init__(self, mix = 'Master', parent = None, i = 0):

		self.Parent = parent
		self.id_ = i

		self.mix = mix

		self.Mixer = alsaaudio.Mixer(self.mix)
		# print self.Mixer.mixer()
		self.capability = self.Mixer.volumecap()
		self.oldValue = self.Mixer.getvolume()
		# print self.oldValue, self.capability

		try :
			self.Mixer.getmute()
			self.Mute_ = QPushButton()
			self.Mute_.setText('Mute')
			Mute = 0
			for i in alsaaudio.Mixer(self.mix).getmute():
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

	def setVolume_timeout(self):
		vol_ = alsaaudio.Mixer(self.mix).getvolume()
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
		for i in alsaaudio.Mixer(self.mix).getmute():
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
			self.setCurrentValue(self.Parent.sliderHPlasma[self.id_])

	def setCurrentValue(self, obj):
		vol_ = int(min(self.oldValue))
		obj.setValue(vol_)
		obj.setToolTip(obj.name + ' ' + str(vol_) + '%')

class FontWidget(QFontDialog):
	def __init__(self, parent = None):
		QFontDialog.__init__(self, parent)

		fontSelect = []

class ColorWidget(QColorDialog):
	def __init__(self, parent = None):
		QColorDialog.__init__(self, parent)

		color = QColorDialog(QColor(QString('red')))
		color.setVisible(True)

class DevicePanel(QWidget):
	def __init__(self, obj = None, parent = None):
		QWidget.__init__(self, parent)

		self.layout = QGridLayout()

		i = 0
		str_raw = (obj.Settings.value('PanelDevices')).toString()
		self.presentDevices = []
		listPanelDevices = string.split(str(str_raw),',')
		for item_ in obj.sliderHandle:
			if (type(item_) is not str) :
				str_ = item_.name
				self.presentDevices += [str_]
				self.presentDevices[i] = QCheckBox(str_)
				self.presentDevices[i].name = str_
				if str_ in listPanelDevices:
					self.presentDevices[i].setCheckState(2)
				self.layout.addWidget(self.presentDevices[i], i, 0)
				i += 1

		self.setLayout(self.layout)

	def refreshPanelDevices(self, obj):
		obj.panelDevices = []
		for item_ in self.presentDevices:
			if item_.isChecked() :
				obj.panelDevices += [item_.name]

		str_ = string.join(obj.panelDevices, ',')
		obj.Settings.setValue('PanelDevices',str_)
		obj.Settings.sync()

class InterfaceSettings(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.layout = QGridLayout()

		i = 0
		self.list_ = []
		for item_ in ['Icon_On', 'Vertical::widgetOrientation']:
		# 'Vertical::panelOrientation',\
			str_ = str((obj.Settings.value(item_)).toString())
			self.list_ += [item_]
			self.list_[i] = QCheckBox(item_)
			self.list_[i].name = item_
			if str_ == '1':
				self.list_[i].setCheckState(2)
			self.layout.addWidget(self.list_[i], i, 0)
			i += 1

		labelDefaultInfo = QLabel()
		labelDefaultInfo.setText('<font color=red><b>Default: Horizontal::widgetOrientation</b></font>')
		self.layout.addWidget(labelDefaultInfo,i,0)

		self.setLayout(self.layout)

	def refreshInterfaceSettings(self, obj):

		for item_ in self.list_:
			if item_.isChecked() :
				obj.Settings.setValue(item_.name, '1')
			else:
				obj.Settings.setValue(item_.name, '0')

		obj.Settings.sync()

try :
	def CreateApplet(parent):
		return plasmaVolume(parent)
except x :
	print x
finally :
	pass

x = ''
Flag = T()
