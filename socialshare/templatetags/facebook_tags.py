from django import template

register = template.Library()


@register.simple_tag
def opengraph_tag(*args, **kwargs):
    """
    Usage:
    {% load facebook_tags %}
    {% opengraph_tag title="My Great Page" [type="website"] %}
    """

    template = '<meta property="og:%(property)s" content="%(val)s" />'
    out = []
    for k, v in kwargs.items():
        out.append(template % {
            'property': k,
            'val': v
        })

    return ''.join(out)
