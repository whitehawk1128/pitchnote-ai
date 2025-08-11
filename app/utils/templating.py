from jinja2 import Template

def render_template(template_str, variables):
    return Template(template_str).render(**variables)