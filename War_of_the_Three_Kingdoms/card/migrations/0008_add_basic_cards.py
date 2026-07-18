from django.db import migrations, models


BASIC_CARDS = [
    ('殺', 'images/basic_card/kill.png'),
    ('閃', 'images/basic_card/dodge.png'),
    ('桃', 'images/basic_card/Recover_HP .png'),
]


def seed_basic_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name, image_path in BASIC_CARDS:
        Card.objects.update_or_create(
            image_path=image_path,
            defaults={
                'name': name,
                'faction': 'Basic',
                'health': 0,
                'skills': [],
            },
        )


def remove_basic_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(image_path__in=[image_path for _, image_path in BASIC_CARDS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0007_add_equipment_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='faction',
            field=models.CharField(choices=[('Chun', '群'), ('Shu', '蜀'), ('Wei', '魏'), ('Wu', '吳'), ('Identity', '身份'), ('Basic', '基本牌'), ('Function', '功能牌'), ('Equipment', '裝備牌')], max_length=16),
        ),
        migrations.RunPython(seed_basic_cards, remove_basic_cards),
    ]
