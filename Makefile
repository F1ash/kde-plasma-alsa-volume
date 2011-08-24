DESTDIR=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-alsa-volume
KAPPS=share/kde4/apps
KSERV=share/kde4/services
PLASMA=plasma/plasmoids
CODE=contents/code
ICONS=contents/icons
STYLE=contents/style

build:
	@echo "Nothing to build"

install: build
	$(INSTALL) metadata.desktop $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	$(INSTALL) $(CODE)/main.py $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(CODE)/main.py
	$(INSTALL) $(STYLE)/style.css $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(STYLE)/style.css
	$(INSTALL) $(STYLE)/style_horiz.css $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(STYLE)/style_horiz.css
	$(INSTALL) $(STYLE)/style_vert.css $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(STYLE)/style_vert.css
	$(INSTALL) $(ICONS)/color.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/color.png
	$(INSTALL) $(ICONS)/play.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/play.png
	$(INSTALL) $(ICONS)/refresh.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/refresh.png
	$(INSTALL) $(ICONS)/sound.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/sound.png
	$(INSTALL) $(ICONS)/sound_min.png $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)/$(ICONS)/sound_min.png

clean:
	rm -rf $(DESTDIR)/$(KSERV)/$(APP_NAME).desktop
	rm -rf $(DESTDIR)/$(KAPPS)/$(PLASMA)/$(APP_NAME)
