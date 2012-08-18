from django import template
from quotes.quotes.models import Quote

register = template.Library()


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
