from django import template
from django.conf import settings
from quotes.quotes.models import Quote

register = template.Library()

from allauth.socialaccount.models import SocialApp


@register.assignment_tag
def get_latest_quote():
    try:
        return Quote.objects.latest('published_on')
    except Quote.DoesNotExist:
        return None


@register.assignment_tag
def get_last_quote_by_index(index):
    try:
        return Quote.objects.all().order_by('-published_on')[index]
    except Quote.DoesNotExist:
        return None

if not settings.DEBUG:
    @register.assignment_tag
    def get_home_quote():
        # XXX this is meant to work only on postgres.
        return Quote.objects.raw('SELECT * FROM quotes_quote ORDER BY'
                                 ' RANDOM()*star_count DESC LIMIT 1')[0]
else:
    @register.assignment_tag
    def get_home_quote():
        return get_latest_quote()


@register.simple_tag
def get_facebook_app_id():
    try:
        return SocialApp.objects.get(name='Facebook').key
    except SocialApp.DoesNotExist:
        return ''
