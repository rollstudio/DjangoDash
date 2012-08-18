from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from .models import Quote, Author
from .forms import QuoteForm


class QuoteDetail(DetailView):
    model = Quote


class QuoteCreate(LoginRequiredMixin, CreateView):
    form_class = QuoteForm
    model = Quote

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.author = Author.objects.get_or_create(name=form.instance.author)

        print 'lol'

        return super(QuoteCreate, self).form_valid(form)
