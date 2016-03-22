"""12/3/2016."""


import sys
import os

from jinja2 import Environment, FileSystemLoader

from posts import Post


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

    out_path_dir = os.path.dirname(out_path)
    if not os.path.exists(out_path_dir):
        os.makedirs(out_path_dir)

    with open(out_path, 'w') as out_f:
        out_f.write(html.encode('utf-8'))


if __name__ == '__main__':
    render_post(sys.argv[1], sys.argv[2])
