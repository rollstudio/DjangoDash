from django import template
from django.conf import settings
from quotes.quotes.models import Quote, UserStar

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

# Since the raw query we're using works only with postgres we do this check to
# make the tag usable with sqlite too.
if not settings.DEBUG:
    @register.assignment_tag
    def get_home_quote():
        """
        Gets a random quote from the ones with the most stars.
        """
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

@register.assignment_tag(takes_context=True)
def get_starred(context):
    """
    Checks if the current user has "starred" or not the current Quote.
    """
    try:
        UserStar.objects.get(user=context['user'], quote=context['quote'])
    except UserStar.DoesNotExist:
        return False
    else:
        return True
