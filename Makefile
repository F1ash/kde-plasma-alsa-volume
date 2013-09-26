PREFIX=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-alsa-volume
KAPPS=share/kde4/apps
KSERV=share/kde4/services
PLASMA=plasma/plasmoids
CODE=contents/code

build:
	@echo "Nothing to build"

install: build
	$(INSTALL) metadata.desktop $(DESTDIR)$(PREFIX)/$(KSERV)/$(APP_NAME).desktop
	$(INSTALL) metadata.desktop $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/metadata.desktop
	$(INSTALL) $(CODE)/AudioOutput.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/AudioOutput.py
	$(INSTALL) $(CODE)/ColorWidget.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/ColorWidget.py
	$(INSTALL) $(CODE)/DevicePanel.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/DevicePanel.py
	$(INSTALL) $(CODE)/InterfaceSettings.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/InterfaceSettings.py
	$(INSTALL) $(CODE)/main.py  $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/main.py
	$(INSTALL) $(CODE)/SensitivitySlider.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/SensitivitySlider.py
	$(INSTALL) $(CODE)/SizeWidget.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/SizeWidget.py
	$(INSTALL) $(CODE)/Style.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/Style.py
	$(INSTALL) $(CODE)/TestSliders.py $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/TestSliders.py

clean:
	rm -rf $(DESTDIR)$(PREFIX)/$(KSERV)/$(APP_NAME).desktop
	rm -rf $(DESTDIR)$(PREFIX)/$(KAPPS)/$(PLASMA)/$(APP_NAME)
