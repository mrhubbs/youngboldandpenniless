# 3/15/16
# This mkfile is responsible for updating all site content which depends on templates
# (e.g. generate HTML from templates, compile less into css).


<mkconfig



CORE=\
    $TEMPLATE_PATH/basepage.jinja\
    $TEMPLATE_PATH/google_analytics.jinja\


all:QV: styles html


<posts.mk


TOP_LEVEL_PAGES=\
    homepage.html\
    about-us.html\
    post-feed.html\
    post-tags.html\
    privacy-policy.html\


html:V: $TOP_LEVEL_PAGES posts tag-pages


tag-pages:VQ: posts
    echo -e "\e[1;94mCreating tag pages ...\e[0m"
    $YBP.build_tags_pages


homepage.html:D: $TEMPLATE_PATH/homepage.jinja $CORE
about-us.html:D: $TEMPLATE_PATH/about-us.jinja $CORE
post-feed.html:D: $TEMPLATE_PATH/post-feed.jinja $TEMPLATE_PATH/posts_list.jinja $TEMPLATE_PATH/post_common.jinja $CORE posts
post-tags.html:D: $TEMPLATE_PATH/post-tags.jinja $TEMPLATE_PATH/posts_list.jinja $TEMPLATE_PATH/post_common.jinja $CORE posts
privacy-policy.html:D: $TEMPLATE_PATH/privacy-policy.jinja $CORE


styles:VQ:
    cd $STYLE_PATH
    $MK styles


styles-clean:VQ:
    cd $STYLE_PATH
    $MK clean


styles-purge:VQ:
    cd $STYLE_PATH
    $MK purge
