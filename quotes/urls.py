from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from braces.views import LoginRequiredMixin

from allauth.account.forms import LoginForm, SignupForm

admin.autodiscover()


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        context['signup_form'] = SignupForm()
        return context

urlpatterns = patterns('',
    # Examples:
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', HomeView.as_view()),
    url(r'^quotes/', include('quotes.quotes.urls')),
    #url(r'^show/(?P<object_id>\d+)$',
    #    'django.views.generic.list_detail.object_detail',
    #    {'queryset': Quote.objects.all()}),
    # url(r'^quotes/', include('quotes.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
