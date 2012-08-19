from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView

from allauth.account.forms import LoginForm, SignupForm

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
    url(r'^$', HomeView.as_view()),
    url(r'^accounts/social/connections/$', RedirectView.as_view(url='/')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^quotes/', include('quotes.quotes.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
