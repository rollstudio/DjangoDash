from django.conf.urls import patterns, url
from django.views.decorators.csrf import csrf_exempt

from .views import QuoteCreate


urlpatterns = patterns('',
    url(r'^add/$', csrf_exempt(QuoteCreate.as_view())),
    #url(r'^view/(?P<pk>\d+)/$', QuoteCreate.as_view()),
)
