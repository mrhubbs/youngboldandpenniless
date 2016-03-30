""" 3-30-16 """


class CleanStringMapping(object):
    def __init__(self, keep):
        keep = unicode(keep)
        self.comp = dict((ord(c), c) for c in keep)

    def __getitem__(self, k):
        return self.comp.get(k)
