from urllib import quote

from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def google_plus_link(text, url):
    """
    Usage:
    {% load google_tags %}
    {% google_plus_link "text for the anchor" url %}
    """

    if not url.startswith('http'):
        try:
            current_site = Site.objects.get_current()
            url = 'http://%s%s' % (current_site.domain, url)
        except Site.DoesNotExist:
            raise template.TemplateSyntaxError('No site set.')

    t = '<a href="https://plus.google.com/share?url=%(url)s">%(text)s</a>'

    return t % {
        'url': quote(url),
        'text': text
    }
