from urllib import quote

from django import template
from django.contrib.sites.models import Site

register = template.Library()


@register.simple_tag
def tweet_link(url_text, *args, **kwargs):
    """
    Usage:
    {% load twitter_tags %}
    {% tweet_link "text for the anchor" url="/" [text="Check my site"] %}
    """

    template = '<a href="https://twitter.com/intent/tweet?%(link)s">%(text)s</a>'
    out = []

    for k, v in kwargs.items():
        if k == 'url' and not v.startswith('http'):
            try:
                current_site = Site.objects.get_current()
                v = 'http://%s%s' % (current_site.domain, v)
            except Site.DoesNotExist:
                raise template.TemplateSyntaxError('No site set.')

        out.append(k + '=' + quote(v.encode('utf-8')))

    return template % {
        'link': '&'.join(out),
        'text': url_text
    }
