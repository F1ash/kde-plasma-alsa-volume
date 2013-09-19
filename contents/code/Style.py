# -*- coding: utf-8 -*-

STYLE_HORYZ = \
'QSlider { \
    margin: __MARGIN__px;  /* aka slider margin*/ \
    min-width: 18px; \
    /* max-width: 35px; */ \
    height: __THICK__px;  /* aka slider thinkness*/ \
    vertical-align: center; \
    position: center; \
} \
 \
QSlider::groove:horizontal { \
    border: 1px solid rgba(0,0,0,0); /* #999999; */ \
    position: absolute; \
    background: rgba(0,0,0,0);  \
    margin: 0 -1px; \
} \
 \
QSlider::handle:horizontal { \
    width: __HTHICK__px;  /* aka handle thinkness*/ \
    border: 1px solid #5c5c5c; \
    background: #CCCCCC; \
    margin: -__HLEDGE__px 0;  /* aka handler ledge : расширяется наружу от бороздки */ \
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
    margin: __MARGIN__px;  /* aka slider margin*/ \
    min-height: 18px; \
    /* max-height: 35px; */ \
    width: __THICK__px;  /* aka slider thinkness*/ \
    vertical-align: center; \
    position: center; \
} \
 \
QSlider::groove:vertical { \
    border: 1px solid #999999; /* last change */ \
    background:  rgba(0,0,0,0);  /* #FFEE55; */ \
    position: absolute; \
    margin: 1px 0 -1px; /* last change */ \
} \
 \
QSlider::handle:vertical { \
    height: __HTHICK__px;  /* aka handle thinkness*/ \
    border: 1px solid #5c5c5c; \
    background: #CCCCCC; \
    margin: 0 -__HLEDGE__px; /* aka handler ledge : расширяется наружу от бороздки */ \
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
