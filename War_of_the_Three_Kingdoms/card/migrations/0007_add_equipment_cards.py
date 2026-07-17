from django.db import migrations, models


EQUIPMENT_CARDS = [
    '丈八蛇矛',
    '八卦陣',
    '寒冰劍',
    '方天化擊',
    '諸葛連弩',
    '貫石斧',
    '進攻馬',
    '雌雄雙股劍',
    '青釭劍',
    '青龍偃月刀',
    '麒麟弓',
]


def seed_equipment_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name in EQUIPMENT_CARDS:
        Card.objects.update_or_create(
            image_path=f'images/Equipment_card/{name}.png',
            defaults={
                'name': name,
                'faction': 'Equipment',
                'health': 0,
                'skills': [],
            },
        )


def remove_equipment_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(
        image_path__in=[f'images/Equipment_card/{name}.png' for name in EQUIPMENT_CARDS]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0006_add_function_cards'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='faction',
            field=models.CharField(choices=[('Chun', '群'), ('Shu', '蜀'), ('Wei', '魏'), ('Wu', '吳'), ('Identity', '身份'), ('Function', '功能牌'), ('Equipment', '裝備牌')], max_length=16),
        ),
        migrations.RunPython(seed_equipment_cards, remove_equipment_cards),
    ]
