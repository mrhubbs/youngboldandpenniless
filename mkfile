# 3/15/16
# This mkfile is responsible for updating all site content which depends on templates
# (e.g. generate HTML from templates, compile less into css).


<mkconfig



CORE=\
    $TEMPLATE_PATH/basepage.jinja\
    $TEMPLATE_PATH/google_analytics.jinja\


all:QV: styles html


<posts.mk


html:V: homepage.html about-us.html posts

homepage.html:D: $TEMPLATE_PATH/homepage.jinja $CORE
about-us.html:D: $TEMPLATE_PATH/about-us.jinja $CORE


styles:VQ:
    cd $STYLE_PATH
    $MK styles


styles-clean:VQ:
    cd $STYLE_PATH
    $MK clean


styles-purge:VQ:
    cd $STYLE_PATH
    $MK purge
