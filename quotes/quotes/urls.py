from django.conf.urls import patterns, url

from .views import QuoteCreate, QuoteDetail, GetQuote, addstar


urlpatterns = patterns('',
    url(r'^add/$', QuoteCreate.as_view(), name='quote-add'),
    url(r'^view/(?P<pk>\d+)/$', QuoteDetail.as_view(), name='quote-detail'),
    url(r'^next/$', GetQuote.as_view(order='id', query='id__gt'), name='get-next-quote'),
    url(r'^prev/$', GetQuote.as_view(order='-id', query='id__lt'), name='get-prev-quote'),
    url(r'^star/$', addstar),
)
