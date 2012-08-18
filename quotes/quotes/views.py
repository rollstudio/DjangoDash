from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from braces.views import LoginRequiredMixin

from .models import Quote
from .forms import QuoteForm

from mongo_hit_counter.utils import insert_hit


class QuoteDetail(DetailView):
    model = Quote

    def get(self, request, *args, **kwargs):
        insert_hit('Quote', str(self.model.pk), request.META['REMOTE_ADDR'])

        return super(QuoteDetail, self).get(request, *args, **kwargs)


class QuoteCreate(LoginRequiredMixin, CreateView):
    form_class = QuoteForm
    model = Quote

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(QuoteCreate, self).form_valid(form)
