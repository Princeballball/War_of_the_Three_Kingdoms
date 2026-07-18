from django.db import migrations, models


STANDARD_COUNTS = {
    '殺': 30,
    '閃': 15,
    '桃': 8,
    '無中生有': 4,
    '過河拆橋': 6,
    '順手牽羊': 5,
    '決鬥': 3,
    '借刀殺人': 2,
    '南蠻入侵': 3,
    '萬箭齊發': 1,
    '五穀豐登': 2,
    '桃園結義': 1,
    '無懈可擊': 4,
    '樂不思蜀': 3,
    '閃電': 2,
    '諸葛連弩': 2,
    '青釭劍': 1,
    '雌雄雙股劍': 1,
    '寒冰劍': 1,
    '青龍偃月刀': 1,
    '丈八蛇矛': 1,
    '貫石斧': 1,
    '方天畫戟': 1,
    '麒麟弓': 1,
    '八卦陣': 2,
    '仁王盾': 1,
    '進攻馬': 3,
    '防禦馬': 3,
}


def standardize_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(name='五穀豐收').update(name='五穀豐登')
    Card.objects.filter(name='方天化擊').update(name='方天畫戟')
    Card.objects.update(deck_count=1)
    for name, count in STANDARD_COUNTS.items():
        Card.objects.filter(name=name).update(deck_count=count)


def reset_counts(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(name='五穀豐登').update(name='五穀豐收')
    Card.objects.filter(name='方天畫戟').update(name='方天化擊')
    Card.objects.update(deck_count=1)


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_add_basic_cards'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='deck_count',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.RunPython(standardize_cards, reset_counts),
    ]
