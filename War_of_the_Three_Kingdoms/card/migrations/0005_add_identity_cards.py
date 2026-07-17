from django.db import migrations, models


IDENTITY_CARDS = [
    ('主公', 'images/identity/Lord.png'),
    ('忠臣', 'images/identity/Loyal Minister.png'),
    ('反賊', 'images/identity/Rebel.png'),
    ('內奸', 'images/identity/Traitor.png'),
]


def seed_identity_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name, image_path in IDENTITY_CARDS:
        Card.objects.update_or_create(
            image_path=image_path,
            defaults={
                'name': name,
                'faction': 'Identity',
                'health': 0,
                'skills': [],
            },
        )


def remove_identity_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(image_path__in=[image_path for _, image_path in IDENTITY_CARDS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0004_card_health_card_skills_seed_card_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='faction',
            field=models.CharField(choices=[('Chun', '群'), ('Shu', '蜀'), ('Wei', '魏'), ('Wu', '吳'), ('Identity', '身份')], max_length=16),
        ),
        migrations.RunPython(seed_identity_cards, remove_identity_cards),
    ]
