from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from allauth.account.forms import LoginForm, SignupForm
from quotes.views import GetQuotes

from .quotes.forms import QuoteForm

admin.autodiscover()


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['signup_form'] = SignupForm()
        context['add_quote_form'] = QuoteForm()
        return context

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', HomeView.as_view()),
    url(r'^quotes/', include('quotes.quotes.urls')),
    url(r'^quotes/next$', GetQuotes.as_view(order='id', query='id__gt'), name='get-next-quote'),
    url(r'^quotes/prev$', GetQuotes.as_view(order='-id', query='id__lt')),
    #url(r'^show/(?P<object_id>\d+)$',
    #    'django.views.generic.list_detail.object_detail',
    #    {'queryset': Quote.objects.all()}),
    # url(r'^quotes/', include('quotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
