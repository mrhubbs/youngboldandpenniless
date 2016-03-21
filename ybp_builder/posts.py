"""

3/15/16
"""


import os
from os.path import join as path_join
import datetime
import calendar


class PostMetadataError(Exception):
    pass


class PostDate(object):
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @property
    def month_name(self):
        return calendar.month_name[self.month]

    @property
    def weekday_name(self):
        weekday = datetime.datetime(self.year, self.month, self.day).weekday()
        return calendar.day_name[weekday]

    @property
    def day_suffix(self):
        day = str(self.day)

        if day.endswith('1'):
            suf = 'st'
        if day.endswith('2'):
            suf = 'nd'
        elif day.endswith('3'):
            suf = 'rd'
        else:
            suf = 'th'

        return suf


class PostMetadata(object):

    @classmethod
    def parse_bool(cls, v):
        """ Converts string to bool. """
        if v.lower() == 'true':
            return True
        else:
            return False

    @classmethod
    def parse_int(cls, i):
        try:
            return int(i)
        except (SyntaxError, ValueError):
            raise PostMetadataError('Integer {} has bad format'.format(i))

    @classmethod
    def parse_date(cls, d):
        spl = d.split('-')
        if len(spl) != 3:
            raise PostMetadata('Date {} has bad format'.format(d))

        date = PostDate(
            cls.parse_int(spl[0]),
            cls.parse_int(spl[1]),
            cls.parse_int(spl[2])
        )

        return date

    @classmethod
    def clean_meta(cls, m):
        return m.lstrip(' \t').rstrip(' \t')

    @classmethod
    def canonicalize_title(cls, title):
        """
        Change a title that is acceptable for the title text into one that can
        be used as a URL.
        """
        return title.replace(' ', '-').replace('&', 'and')

    @classmethod
    def process_tag(cls, tag):
        tag = cls.clean_meta(tag)
        tag = tag.replace(' ', '-').lower()
        return tag

    # TODO: include post name in exceptions
    @classmethod
    def parse_metadata(cls, post_text, post_path):
        """
        Find and parse the post metadata.

        Some metadata will default and need not be specified, others are required.
        """

        # Provide defaults for metadata which is not required.
        meta = {
            'author':           u'',
            'disable_ads':      u'False',
            'disable_comments': u'False',
            'tags':             [],
        }
        required_meta = ['title', 'date']

        opening_tag = '<metadata>'
        closing_tag = '</metadata>'

        sidx = post_text.find(opening_tag)
        if sidx < 0:
            raise PostMetadataError('Cannot find post opening metadata tag')

        eidx = post_text.find(closing_tag, sidx + 1)
        if eidx < 0:
            raise PostMetadataError('Cannot find post closing metadata tag')
        eidx += len(closing_tag)

        # get and process the metadata section
        raw_meta = post_text[sidx:eidx]
        raw_meta = raw_meta.splitlines()[1:-1]
        for m in raw_meta:
            spl = m.split('=', 1)
            if len(spl) < 2:
                continue

            key, val = spl
            key = key.lstrip(' \t').rstrip(' \t')

            # process tags
            if key == 'tags':
                val = [cls.process_tag(v) for v in val.split(',')]
            else:
                val.lstrip(' \t').rstrip(' \t')

            meta[key] = val

        for req in required_meta:
            if req not in meta:
                raise PostMetadataError('Post metadata does not have {}'.format(req))

        # process url and identifier
        abs_in_path = os.path.abspath(post_path)
        url_stub = abs_in_path.split('_templates')[1][:-2] + 'html'
        url = 'http://www.youngboldandpenniless.com' + url_stub
        meta['url'] = url
        meta['url_stub'] = url_stub
        meta['identifier'] = url_stub

        # Convert bool values from string to boolean.
        meta['disable_ads'] = PostMetadata.parse_bool(meta['disable_ads'])
        meta['disable_comments'] = \
            PostMetadata.parse_bool(meta['disable_comments'])

        meta['date'] = PostMetadata.parse_date(meta['date'])

        # remove the metadata section from the post
        post_text = post_text[:sidx] + post_text[eidx:]

        return meta, post_text


class Post(object):
    def __init__(self, meta, text):
        self.meta = meta
        self.text = text

    @classmethod
    def from_file(cls, fpath):
        """ Creates a Post instance from a .md template. """
        with open(fpath, 'r') as post_file:
            text = post_file.read().decode('utf-8')
            meta, text = PostMetadata.parse_metadata(text, fpath)

            return cls(meta, text)

    @property
    def blurb(self):
        """ Return first 50 words of text. """
        # Assumes anything separated by a space is a word
        return u' '.join(self.text.split(' ')[:50]) + '...'


def iter_post_templates(work_path, path_stub='', want_ext='.md'):
    """ Recursively search given path for posts. """

    res = []

    for f in os.listdir(work_path):
        fp = path_join(work_path, f)

        # Build subdirectory.
        if os.path.isdir(fp):
            res.extend(
                iter_post_templates(
                    fp,
                    path_stub=path_join(path_stub, f),
                    want_ext=want_ext))
            continue

        if not f.endswith(want_ext) or f.lower() == 'readme.md':
            continue

        res.append(path_join(path_stub, f))

    return res


""" Object for searching and querying posts. """
def search(work_path='./static/_templates/posts'):
    return iter_post_templates(work_path)


def make_posts(path_stubs, work_path='./static/_templates/posts'):
    res = []

    for f in path_stubs:
        fpath = path_join(work_path, f)
        res.append(Post.from_file(fpath))

    return res


def get_date_for_sort(post):
    d = post.meta['date']
    return (d.year, d.month, d.day)


def sort_posts_by_date(posts):
    posts = sorted(posts, key=get_date_for_sort, reverse=True)
    return posts
