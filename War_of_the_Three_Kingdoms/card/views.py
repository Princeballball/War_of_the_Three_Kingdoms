from django.views.generic import ListView

from .models import Card


class CardLibraryView(ListView):
    model = Card
    template_name = 'card/library.html'
    context_object_name = 'cards'

    def get_queryset(self):
        return Card.objects.order_by('faction', 'name')
