"""Generic code to render jinja template to html."""


from jinja2 import Environment, FileSystemLoader

import posts


def render_template(template_path, template_fname, context):
    """Render the given template, using the Jinja engine."""
    template_environment = Environment(
        autoescape=False,
        loader=FileSystemLoader(template_path),
        trim_blocks=False
    )

    return template_environment.get_template(
        template_fname
    ).render(context)


if __name__ == '__main__':
    import sys

    with open(sys.argv[3], 'w') as out_file:
        html = render_template(sys.argv[1], sys.argv[2], {'post_mod': posts})
        out_file.write(html.encode('utf-8'))
