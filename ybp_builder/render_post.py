"""12/3/2016."""


import sys

from jinja2 import Environment, FileSystemLoader

import posts
from posts import Post, makedirs


template_environment = Environment(
    autoescape=False,
    loader=FileSystemLoader('./static/_templates'),
    trim_blocks=False
)


class PostError(Exception):
    pass


def process_html(html, context):
    # append and pre-pend template directives to HTML
    html = '{% extends "post.jinja" %}\n{% block post %}\n' + html + \
        '\n{% endblock post %}'

    templ = template_environment.from_string(html)

    # TODO: standardize this
    context['post_mod'] = posts

    return templ.render(**context)


def render_post(in_path, out_path):
    """
    Renders a post from markdown to a Jinja template, then renders that
    template.
    """

    # read file contents and decode to unicode
    post = Post.from_file(in_path)
    # process markdown
    html = post.process_markdown()
    html = process_html(html, {'post': post})

    # print(meta)

    makedirs(out_path)

    with open(out_path, 'w') as out_f:
        out_f.write(html.encode('utf-8'))


if __name__ == '__main__':
    render_post(sys.argv[1], sys.argv[2])
