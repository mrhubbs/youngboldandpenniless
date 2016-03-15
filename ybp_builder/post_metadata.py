"""

3/15/16
"""


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
