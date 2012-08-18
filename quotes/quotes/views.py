from django.views.generic.edit import CreateView

from .models import Quote
from .forms import QuoteForm


class QuoteCreate(CreateView):
    #form_class = QuoteForm
    model = Quote

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(QuoteCreate, self).form_valid(form)
