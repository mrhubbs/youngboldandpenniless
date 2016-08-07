#!/bin/sh

# Use this instead of the mkfile directly, as we always need to generate posts.mk first.

python -m ybp_builder.build_post_deps ./static/_templates/posts posts.mk
/usr/lib/plan9/bin/mk $1 $2 $3 $4 $5
