"""Young, Bold, and Penniless website builder."""


import os
import shutil
from jinja2 import Environment, FileSystemLoader


class YBPBuilder(object):
    """Young, Bold, and Penniless website builder.

    This object contains the functionality and logic to build the templates
    into the static site.

    There are a few intricacies, such as blah blah blah....
    """

    def __init__(self, base_path, template_path):
        """Initialize."""
        self.base_path = os.path.abspath(base_path)
        self.template_path = os.path.abspath(template_path)

        self.template_environment = Environment(
            autoescape=False,
            loader=FileSystemLoader(template_path),
            trim_blocks=False
        )

    def render_template(self, template_fname, context):
        """Render the given template, using the Jinja engine."""
        return self.template_environment.get_template(
            template_fname
        ).render(context)

    def clean(self):
        """
        Pre-build clean.

        Currently, remove posts directory to ensure no posts deleted from
        templates linger.
        """
        post_path = os.path.join(self.base_path, 'posts')
        if os.path.exists(post_path):
            shutil.rmtree(post_path)

    def _build_ignore(self, prefix_path):
        ignore = []
        path = os.path.join(self.template_path, prefix_path)
        path = os.path.join(path, 'ignore.list')

        try:
            with open(path, 'r') as f:
                for fname in f.readlines():
                    fname = fname.rstrip('\n\r')
                    if fname != '':
                        ignore.append(fname)
        except IOError:
            return []

        return ignore

    def build(self, prefix_path=''):
        """Build all the templates."""

        work_path = os.path.join(self.template_path, prefix_path)
        ignore = self._build_ignore(work_path)

        for f in os.listdir(work_path):
            # Build subdirectory.
            if os.path.isdir(os.path.join(work_path, f)):
                self.build(os.path.join(prefix_path, f))

            if not f.endswith('.html') or f in ignore:
                continue

            # Path of the template we are rendering.
            template_fpath = os.path.join(work_path, f)

            out_fname = os.path.basename(template_fpath)
            out_fpath = \
                os.path.join(
                    os.path.join(self.base_path, prefix_path),
                    out_fname)

            temp_fpath = os.path.join(prefix_path, out_fname)
            print("{: <50} {{}} > {}".format(
                os.path.join(prefix_path, out_fname),
                temp_fpath))

            out_path = os.path.dirname(out_fpath)
            if not os.path.exists(out_path):
                os.makedirs(out_path)

            with open(out_fpath, 'w') as out_f:
                html = self.render_template(
                    temp_fpath,
                    {'page_name': f, 'use_ads': True})
                out_f.write(html.encode('utf-8'))


if __name__ == '__main__':
    import sys
    ybpbuilder = YBPBuilder(sys.argv[1], sys.argv[2])
    ybpbuilder.clean()
    ybpbuilder.build()
