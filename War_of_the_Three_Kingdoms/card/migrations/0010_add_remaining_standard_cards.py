from django.db import migrations


REMAINING_CARDS = [
    ('樂不思蜀', 'Function', 'images/Function_card/樂不思蜀.png', 3),
    ('閃電', 'Function', 'images/Function_card/閃電.png', 2),
    ('仁王盾', 'Equipment', 'images/Function_card/仁王噸.png', 1),
    ('防禦馬', 'Equipment', 'images/Function_card/防禦馬.png', 3),
]


def seed_remaining_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name, faction, image_path, deck_count in REMAINING_CARDS:
        Card.objects.update_or_create(
            image_path=image_path,
            defaults={
                'name': name,
                'faction': faction,
                'health': 0,
                'deck_count': deck_count,
                'skills': [],
            },
        )


def remove_remaining_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(image_path__in=[image_path for _, _, image_path, _ in REMAINING_CARDS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_card_deck_count_standard_counts'),
    ]

    operations = [
        migrations.RunPython(seed_remaining_cards, remove_remaining_cards),
    ]
