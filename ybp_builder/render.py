"""12/3/2016."""


import sys

from jinja2 import Environment, FileSystemLoader
import markdown
import htmlmin

import posts


template_environment = Environment(
    autoescape=False,
    loader=FileSystemLoader('./static/_templates'),
    trim_blocks=False
)


def render_markdown(text):
    """ Renders the given text to html from markdown. """

    # 'markdown.extensions.smarty'])
    return markdown.markdown(
        text,
        output_format='html5',
        extensions=['markdown.extensions.nl2br',
                    'markdown.extensions.sane_lists'])


def render_post(in_path, out_path):
    """
    Renders a post from markdown to a Jinja template, then renders that
    template.
    """

    # read file contents and decode to unicode
    post = posts.Post.from_file(in_path)
    # process markdown
    simple_html = post.process_markdown()
    html = process_html_for_post(simple_html, {'post': post})

    # print(meta)

    posts.makedirs(out_path)

    with open(out_path, 'w') as out_f:
        out_f.write(html.encode('utf-8'))


def process_html_for_post(html, context):
    # append and pre-pend template directives to HTML
    html = '{% extends "post.jinja" %}\n{% block post %}\n' + html + \
    '\n{% endblock post %}'

    templ = template_environment.from_string(html)

    # TODO: standardize this
    context['post_mod'] = posts

    rendered = templ.render(**context)

    return htmlmin.minify(rendered, remove_empty_space=True)


if __name__ == '__main__':
    render_post(sys.argv[1], sys.argv[2])
