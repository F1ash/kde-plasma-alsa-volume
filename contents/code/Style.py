# -*- coding: utf-8 -*-

STYLE_HORYZ = \
'QSlider { \
	margin: 3px; \
	min-width: 18px; \
	/* max-width: 35px; */ \
	height: 5px; \
	vertical-align: center; \
	position: center; \
} \
 \
QSlider::groove:horizontal { \
	border: 1px solid rgba(0,0,0,0); /* #999999; */ \
	position: absolute; \
	/* height: 3px; /* по умолчанию бороздка расширяется до размеров ползунка. задав высоту она принимает фиксированный размер */ \
	background: rgba(0,0,0,0);  /* #FFEE55; */ /* qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #B1B1B1, stop:1 #c4c4c4); */ \
	margin: 0 -1px; \
} \
 \
QSlider::handle:horizontal { \
	background: rgba(0,0,0,0); /* #CCCCCC; qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f); */ \
	border: 1px solid #5c5c5c; \
	width: 3px; \
	margin: -3px 0; /* рукоятка располагается по умолчанию в прямоугольнике содержимого бороздки. Расширяется наружу от бороздки */ \
	border-radius: 3px; \
} \
 \
QSlider::add-page:horizontalcal { \
	background: #FFF777; \
} \
 \
QSlider::sub-page:horizontal { \
	background: #2277FF; \
} \
 \
'
STYLE_VERT = \
'QSlider { \
	margin: 3px; \
	min-height: 18px; \
	/* max-height: 35px; */ \
	width: 5px; \
	vertical-align: center; \
	position: center; \
} \
 \
QSlider::groove:vertical { \
	border: 1px solid #999999; /* last change */ \
	background:  rgba(0,0,0,0);  /* #FFEE55; */ \
	position: absolute; /* абсолютная позиция в 4px слева и справа от виджета. установка полей виджета также будет работать... */ \
	/* left: 4px; right: 4px; */ \
	margin: 1px 0 -1px; /* last change */ \
} \
 \
QSlider::handle:vertical { \
	height: 5px; \
	border: 1px solid #5c5c5c; \
	background: #CCCCCC; \
	margin: 0 -3px; /* расширяется наружу от бороздки */ \
	border-radius: 3px; \
} \
 \
QSlider::add-page:vertical { \
	background: #2277FF; \
} \
 \
QSlider::sub-page:vertical { \
	background: #FFF777; \
} \
'
