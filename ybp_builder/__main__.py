"""Young, Bold, and Penniless website builder."""


import os
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

    def _build_ignore(self):
        ignore = []
        with open(os.path.join(self.template_path, 'ignore.list'), 'r') as f:
            for fname in f.readlines():
                fname = fname.rstrip('\n\r')
                if fname != '':
                    ignore.append(fname)

        return ignore

    def build(self):
        """Build all the templates."""
        ignore = self._build_ignore()
        for f in os.listdir(self.template_path):
            if not f.endswith('.html') or f in ignore:
                continue

            template_fpath = os.path.join(self.template_path, f)

            out_fname = os.path.basename(template_fpath)
            out_fpath = os.path.join(self.base_path, out_fname)

            print("{: <20} {{}} > {}".format(out_fname, out_fname))

            with open(out_fpath, 'w') as out_f:
                html = self.render_template(out_fname, {'page_name': f})
                out_f.write(html)


if __name__ == '__main__':
    import sys
    ybpbuilder = YBPBuilder(sys.argv[1], sys.argv[2])
    ybpbuilder.build()
