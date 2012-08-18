from django.conf.urls import patterns, url

from .views import QuoteCreate, QuoteDetail


urlpatterns = patterns('',
    url(r'^add/$', QuoteCreate.as_view(), name='quote-add'),
    url(r'^view/(?P<pk>\d+)/$', QuoteDetail.as_view(), name='quote-detail'),
)
