"""
3-23-16

The functionality here scans all posts, sorts them by tag, and then generates
a page containing all the posts for each tag.
"""


import os

from posts import (generate_tags_mapping, makedirs, PostMetadata)
from render_html import render_template


def build_tags_pages():
    tags_dict = generate_tags_mapping()

    # Create a page for each tag.
    for tag, posts in tags_dict.items():
        page_url = PostMetadata.urlify_tag(tag) + '.html'
        page_url = 'posts/tags/' + page_url

        html = render_template(
            './static/_templates',
            'post-tag-feed.jinja',
            {'posts': posts,
             'tag_name': tag,
             'page_url': '/' + page_url})

        makedirs(page_url)

        with open(page_url, 'w') as page_file:
            page_file.write(html.encode('utf-8'))

    return tags_dict


if __name__ == '__main__':
    # Start by removing all the tag pages.
    os.system("rm -f ./posts/tags/*.html")
    # Now re-build them.
    tags_dict = build_tags_pages()
