from django.views.generic import ListView
from django.db.models import Case, IntegerField, Value, When

from .models import Card


class CardLibraryView(ListView):
    model = Card
    template_name = 'card/library.html'
    context_object_name = 'cards'

    def get_queryset(self):
        faction_order = Case(
            When(faction=Card.Faction.IDENTITY, then=Value(0)),
            When(faction=Card.Faction.FUNCTION, then=Value(1)),
            When(faction=Card.Faction.WEI, then=Value(2)),
            When(faction=Card.Faction.SHU, then=Value(3)),
            When(faction=Card.Faction.WU, then=Value(4)),
            When(faction=Card.Faction.CHUN, then=Value(5)),
            default=Value(6),
            output_field=IntegerField(),
        )
        return Card.objects.annotate(faction_order=faction_order).order_by('faction_order', 'name')
