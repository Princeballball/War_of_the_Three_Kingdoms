from django.db import migrations, models


FUNCTION_CARDS = [
    '五穀豐收',
    '借刀殺人',
    '南蠻入侵',
    '桃園結義',
    '決鬥',
    '無中生有',
    '無懈可擊',
    '萬箭齊發',
    '過河拆橋',
    '順手牽羊',
]


def seed_function_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name in FUNCTION_CARDS:
        Card.objects.update_or_create(
            image_path=f'images/Function_card/{name}.png',
            defaults={
                'name': name,
                'faction': 'Function',
                'health': 0,
                'skills': [],
            },
        )


def remove_function_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(
        image_path__in=[f'images/Function_card/{name}.png' for name in FUNCTION_CARDS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_add_identity_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='faction',
            field=models.CharField(choices=[('Chun', '群'), ('Shu', '蜀'), ('Wei', '魏'), ('Wu', '吳'), ('Identity', '身份'), ('Function', '功能牌')], max_length=16),
        ),
        migrations.RunPython(seed_function_cards, remove_function_cards),
    ]
