from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic import ListView

from card.models import Card


def index(request):
    return HttpResponse(Card.objects.all())


class CardListView(ListView):
    model = Card
    template_name = 'card/index.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.all()


# DetailView by slug
class CardDetailView(DetailView):
    model = Card
    template_name = 'card/card.html'
    context_object_name = 'card'

    def get_queryset(self):
        return Card.objects.filter(slug=self.kwargs['slug'])
