from django.core import serializers
from django.http import HttpResponse, Http404
from django.db.models import ObjectDoesNotExist
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import BaseListView

from braces.views import LoginRequiredMixin

from .models import Quote, Author, UserStar
from .forms import QuoteForm


class QuoteDetail(DetailView):
    model = Quote


class QuoteCreate(LoginRequiredMixin, CreateView):
    form_class = QuoteForm
    model = Quote

    def form_valid(self, form):
        form.instance.user = self.request.user
        author = form.cleaned_data['author_field'].strip()

        if author:
            form.instance.author, created = Author.objects.get_or_create(name=author)

        return super(QuoteCreate, self).form_valid(form)


class GetQuotes(BaseListView):
    limit = 5
    order = None
    query = None

    def get_queryset(self):

        try:
            id = self.request.GET['id']
        except KeyError:
            raise Http404
        limit = self.request.GET.get('limit', self.limit)

        return Quote.objects.filter(**{self.query: id}).order_by(self.order)[:limit]

    def render_to_response(self, context):
        content = serializers.serialize("json", context['object_list'])
        return HttpResponse(content, content_type='application/json')


class GetQuote(DetailView):

    order = None
    query = None
    queryset = Quote.objects.all()
    pk_url_kwarg = 'id'
    template_name = 'quotes/quote.html'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        try:
            pk = self.request.GET[self.pk_url_kwarg]
        except KeyError:
            raise AttributeError("GetQuote must be called with an object pk.")

        try:
            obj = queryset.filter(**{self.query: pk}).order_by(self.order)[0]
        except (ObjectDoesNotExist, IndexError):
            raise Http404

        return obj


def manage_star(request, add=True):
    try:
        id = int(request.REQUEST['id'])
    except (KeyError, ValueError):
        raise Http404("Invalid id")

    if not request.user.is_authenticated():
        return HttpResponse("2", status=403,
                            content_type='application/json')

    try:
        quote = Quote.objects.get(id=id)
    except Quote.DoesNotExist:
        raise Http404("Quote object not found")

    try:
        if add:
            UserStar.objects.create(user=request.user, quote=quote)
        else:
            UserStar.objects.get(user=request.user, quote=quote).delete()
    except:  # IntegrityError
        return HttpResponse("0", content_type='application/json')
    else:
        return HttpResponse("1", content_type='application/json')
