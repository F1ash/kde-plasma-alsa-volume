DESTDIR=/usr
INSTALL=install -D -m 0644 -p
APP_NAME=kde-plasma-alsa-volume
PLASMA=plasma/plasmoids

build:
	@echo "Nothing to build"

install: build
	$(INSTALL) metadata.desktop $(DESTDIR)/share/kde4/services/$(APP_NAME).desktop
	$(INSTALL) contents/code/main.py $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/code/main.py
	$(INSTALL) contents/code/getText.sh $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/style/style.css
	$(INSTALL) contents/code/getText.sh $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/style/style_horiz.css
	$(INSTALL) contents/code/getText.sh $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/style/style_vert.css
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/color.png
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/play.png
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/refresh.png
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/sound.png
	$(INSTALL) contents/icons/advice.png $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)/icons/sound_min.png

clean:
	rm -rf $(DESTDIR)/share/kde4/services/$(APP_NAME).desktop
	rm -rf $(DESTDIR)/share/kde4/apps/$(PLASMA)/$(APP_NAME)
