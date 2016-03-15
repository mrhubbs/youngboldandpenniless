"""12/3/2016."""


import sys
import os

import markdown
from jinja2 import Environment, FileSystemLoader

from post_metadata import PostMetadata


template_environment = Environment(
    autoescape=False,
    loader=FileSystemLoader('./static/_templates'),
    trim_blocks=False
)


class PostError(Exception):
    pass


def process_tag(tag):
    tag = PostMetadata.clean_meta(tag)
    tag = tag.replace(' ', '-')
    return tag


# TODO: include post name in exceptions
def parse_metadata(post):
    """
    Find and parse the post metadata.

    Some metadata will default and need not be specified, others are required.
    """

    # Provide defaults for metadata which is not required.
    meta = {
        'author':           u'',
        'disable_ads':      u'False',
        'disable_comments': u'False',
    }
    required_meta = ['title', 'date']

    opening_tag = '<metadata>'
    closing_tag = '</metadata>'

    sidx = post.find(opening_tag)
    if sidx < 0:
        raise PostError('Cannot find post opening metadata tag')

    eidx = post.find(closing_tag, sidx + 1)
    if eidx < 0:
        raise PostError('Cannot find post closing metadata tag')
    eidx += len(closing_tag)

    # get and process the metadata section
    raw_meta = post[sidx:eidx]
    raw_meta = raw_meta.splitlines()[1:-1]
    for m in raw_meta:
        spl = m.split('=', 1)
        if len(spl) < 2:
            continue

        key, val = spl
        key = key.lstrip(' \t').rstrip(' \t')

        if key == 'tags':
            val = [process_tag(v) for v in val.split(',')]
        else:
            val.lstrip(' \t').rstrip(' \t')

        meta[key] = val

    for req in required_meta:
        if req not in meta:
            raise PostError('Post metadata does not have {}'.format(req))

    # Convert bool values from string to boolean.
    meta['disable_ads'] = PostMetadata.parse_bool(meta['disable_ads'])
    meta['disable_comments'] = \
        PostMetadata.parse_bool(meta['disable_comments'])

    meta['date'] = PostMetadata.parse_date(meta['date'])

    # remove the metadata section from the post
    post = post[:sidx] + post[eidx:]

    return meta, post


def process_markdown(md):

    meta, md = parse_metadata(md)

    return meta, markdown.markdown(
        md,
        output_format='html5',
        extensions=['markdown.extensions.nl2br',
                    'markdown.extensions.sane_lists',
                    'markdown.extensions.smarty'])


def process_html(html, context):
    # append and pre-pend template directives to HTML
    html = '{% extends "post.html" %}\n{% block post %}\n' + html + \
        '\n{% endblock post %}'

    templ = template_environment.from_string(html)

    return templ.render(**context)


def render_post(in_path, out_path):
    """
    Renders a post from markdown to a Jinja template, then renders that
    template.
    """
    abs_in_path = os.path.abspath(in_path)
    url_stub = abs_in_path.split('_templates')[1]
    url = 'http://www.youngboldandpenniless.com/blog/' + url_stub

    with open(in_path, 'r') as in_f:
        # read file contents and decode to unicode
        md = in_f.read().decode('utf-8')
        # process markdown
        meta, html = process_markdown(md)
        meta['url'] = url
        meta['identifier'] = url_stub
        print(meta)
        html = process_html(html, meta)

        with open(out_path, 'w') as out_f:
            out_f.write(html.encode('utf-8'))


if __name__ == '__main__':
    render_post(sys.argv[1], sys.argv[2])
