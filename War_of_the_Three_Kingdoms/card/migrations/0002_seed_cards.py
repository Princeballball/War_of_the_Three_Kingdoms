from django.db import migrations


CARDS = [
    ('貂蟬', 'Chun', 'images/card/Chun/Diao_Chan.png'),
    ('華佗', 'Chun', 'images/card/Chun/Hua_Tuo.png'),
    ('華雄', 'Chun', 'images/card/Chun/Hua_Xiong.png'),
    ('呂布', 'Chun', 'images/card/Chun/Lu_Bu.png'),
    ('袁術', 'Chun', 'images/card/Chun/Yuan_Shu.png'),
    ('關羽', 'Shu', 'images/card/Shu/Guan_Yu.png'),
    ('黃月英', 'Shu', 'images/card/Shu/Huang_Yueying.png'),
    ('劉備', 'Shu', 'images/card/Shu/Liu_Bei.png'),
    ('馬超', 'Shu', 'images/card/Shu/Ma_Chao.png'),
    ('張飛', 'Shu', 'images/card/Shu/Zhang_Fei.png'),
    ('趙雲', 'Shu', 'images/card/Shu/Zhao_Yun.png'),
    ('諸葛亮', 'Shu', 'images/card/Shu/Zhuge_Liang.png'),
    ('曹操', 'Wei', 'images/card/Wei/Cao_Cao.png'),
    ('郭嘉', 'Wei', 'images/card/Wei/Guo_Jia.png'),
    ('司馬懿', 'Wei', 'images/card/Wei/Sima_Yi.png'),
    ('夏侯惇', 'Wei', 'images/card/Wei/Xiahou_Dun.png'),
    ('許褚', 'Wei', 'images/card/Wei/Xu_Chu.png'),
    ('張遼', 'Wei', 'images/card/Wei/Zhang_Liao.png'),
    ('甄姬', 'Wei', 'images/card/Wei/Zhen_Ji.png'),
    ('大喬', 'Wu', 'images/card/Wu/Da_Qiao.png'),
    ('甘寧', 'Wu', 'images/card/Wu/Gan_Ning.png'),
    ('黃蓋', 'Wu', 'images/card/Wu/Huang_Gai.png'),
    ('呂蒙', 'Wu', 'images/card/Wu/Lu_Meng.png'),
    ('陸遜', 'Wu', 'images/card/Wu/Lu_Xun.png'),
    ('孫權', 'Wu', 'images/card/Wu/Sun_Quan.png'),
    ('孫尚香', 'Wu', 'images/card/Wu/Sun_Shangxiang.png'),
    ('周瑜', 'Wu', 'images/card/Wu/Zhou_Yu.png'),
]


def seed_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for name, faction, image_path in CARDS:
        Card.objects.update_or_create(
            image_path=image_path,
            defaults={'name': name, 'faction': faction},
        )


def remove_seeded_cards(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(image_path__in=[image_path for _, _, image_path in CARDS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_cards, remove_seeded_cards),
    ]
