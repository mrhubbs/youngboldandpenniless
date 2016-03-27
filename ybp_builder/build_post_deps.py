"""Iterates the post templates to construct a mkfile for building the posts."""


import os
from os.path import join as path_join
import shutil

from posts import iter_post_templates


post_deps = "$TEMPLATE_PATH/post.jinja $TEMPLATE_PATH/post_common.jinja $CORE"


def build_rules(template_path, templs):
    rules = []
    targets = []

    for t in templs:
        target = 'posts/{0}.html'.format(os.path.splitext(t)[0])
        rule = '{0}:Q: $TEMPLATE_PATH/posts/{1} {2}'.format(
            target, t, post_deps)
        rules.append(rule)
        targets.append(target)

    return rules, targets


def write_mkfile(rules, targets, posts_to_prune):
    res = \
"""
# AUTO-GENERATED: DO NOT HAND EDIT
#
# This file contains rules for building each post from its template.
\n"""

    for r in rules:
        res += r + '\n'

    res += \
"""
posts:VQ: {} prune-posts
    echo -e "\e[1;94mPosts up to date\e[0m"
    # Always delete this so we can't accidentally use an old version.
    rm -f posts.mk
""".format(' '.join(targets))

    res += "prune-posts:VQ:"

    if len(posts_to_prune) < 1:
        res += \
"""
    echo -e "\e[1;94mNo posts to prune\e[0m"
"""
    else:
        res += \
"""
    echo -e "\e[1;94mPruning posts...\e[0m"
    echo -e "\e[1;91mrm -f {0} ...\e[0m"
    rm -f {0}
""".format(' '.join(posts_to_prune))

    return res


if __name__ == '__main__':
    import sys

    posts_path = sys.argv[1]
    out_path = sys.argv[2]

    # Generate data for post template rules.
    template_posts = iter_post_templates(posts_path)
    rules, targets = build_rules(posts_path, template_posts)

    # Generate data for post prune rule.
    rendered_posts = iter_post_templates('./posts/', want_ext='.html')
    # Filter out the tag pages.
    rendered_posts = filter(lambda x: not x.startswith('tags'), rendered_posts)
    rendered_posts_set = {c[:-5] for c in rendered_posts}
    template_posts_set = {t[:-3] for t in template_posts}

    posts_to_prune = rendered_posts_set - template_posts_set
    posts_to_prune = ['posts/' + p + '.html' for p in posts_to_prune]

    with open(out_path, 'w') as out_f:
        out_f.write(write_mkfile(rules, targets, posts_to_prune))
