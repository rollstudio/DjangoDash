from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def opengraph_tag(*args, **kwargs):
    """
    Usage:
    {% load facebook_tags %}
    {% opengraph_tag title="My Great Page" [type="website"] %}
    """

    t = '<meta property="og:%(property)s" content="%(val)s" />'
    out = []
    for k, v in kwargs.items():
        if k == 'url' and not v.startswith('http'):
            try:
                current_site = Site.objects.get_current()
                v = 'http://%s%s' % (current_site.domain, v)
            except Site.DoesNotExist:
                raise template.TemplateSyntaxError('No site set.')

        out.append(t % {
            'property': k,
            'val': v
        })

    return ''.join(out)
