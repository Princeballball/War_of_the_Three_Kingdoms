from django.db import migrations


CARD_NAMES = {
    'images/card/Chun/Diao_Chan.png': '貂蟬',
    'images/card/Chun/Hua_Tuo.png': '華佗',
    'images/card/Chun/Hua_Xiong.png': '華雄',
    'images/card/Chun/Lu_Bu.png': '呂布',
    'images/card/Chun/Yuan_Shu.png': '袁術',
    'images/card/Shu/Guan_Yu.png': '關羽',
    'images/card/Shu/Huang_Yueying.png': '黃月英',
    'images/card/Shu/Liu_Bei.png': '劉備',
    'images/card/Shu/Ma_Chao.png': '馬超',
    'images/card/Shu/Zhang_Fei.png': '張飛',
    'images/card/Shu/Zhao_Yun.png': '趙雲',
    'images/card/Shu/Zhuge_Liang.png': '諸葛亮',
    'images/card/Wei/Cao_Cao.png': '曹操',
    'images/card/Wei/Guo_Jia.png': '郭嘉',
    'images/card/Wei/Sima_Yi.png': '司馬懿',
    'images/card/Wei/Xiahou_Dun.png': '夏侯惇',
    'images/card/Wei/Xu_Chu.png': '許褚',
    'images/card/Wei/Zhang_Liao.png': '張遼',
    'images/card/Wei/Zhen_Ji.png': '甄姬',
    'images/card/Wu/Da_Qiao.png': '大喬',
    'images/card/Wu/Gan_Ning.png': '甘寧',
    'images/card/Wu/Huang_Gai.png': '黃蓋',
    'images/card/Wu/Lu_Meng.png': '呂蒙',
    'images/card/Wu/Lu_Xun.png': '陸遜',
    'images/card/Wu/Sun_Quan.png': '孫權',
    'images/card/Wu/Sun_Shangxiang.png': '孫尚香',
    'images/card/Wu/Zhou_Yu.png': '周瑜',
}


ENGLISH_NAMES = {
    'images/card/Chun/Diao_Chan.png': 'Diao Chan',
    'images/card/Chun/Hua_Tuo.png': 'Hua Tuo',
    'images/card/Chun/Hua_Xiong.png': 'Hua Xiong',
    'images/card/Chun/Lu_Bu.png': 'Lu Bu',
    'images/card/Chun/Yuan_Shu.png': 'Yuan Shu',
    'images/card/Shu/Guan_Yu.png': 'Guan Yu',
    'images/card/Shu/Huang_Yueying.png': 'Huang Yueying',
    'images/card/Shu/Liu_Bei.png': 'Liu Bei',
    'images/card/Shu/Ma_Chao.png': 'Ma Chao',
    'images/card/Shu/Zhang_Fei.png': 'Zhang Fei',
    'images/card/Shu/Zhao_Yun.png': 'Zhao Yun',
    'images/card/Shu/Zhuge_Liang.png': 'Zhuge Liang',
    'images/card/Wei/Cao_Cao.png': 'Cao Cao',
    'images/card/Wei/Guo_Jia.png': 'Guo Jia',
    'images/card/Wei/Sima_Yi.png': 'Sima Yi',
    'images/card/Wei/Xiahou_Dun.png': 'Xiahou Dun',
    'images/card/Wei/Xu_Chu.png': 'Xu Chu',
    'images/card/Wei/Zhang_Liao.png': 'Zhang Liao',
    'images/card/Wei/Zhen_Ji.png': 'Zhen Ji',
    'images/card/Wu/Da_Qiao.png': 'Da Qiao',
    'images/card/Wu/Gan_Ning.png': 'Gan Ning',
    'images/card/Wu/Huang_Gai.png': 'Huang Gai',
    'images/card/Wu/Lu_Meng.png': 'Lu Meng',
    'images/card/Wu/Lu_Xun.png': 'Lu Xun',
    'images/card/Wu/Sun_Quan.png': 'Sun Quan',
    'images/card/Wu/Sun_Shangxiang.png': 'Sun Shangxiang',
    'images/card/Wu/Zhou_Yu.png': 'Zhou Yu',
}


def localize_names(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for image_path, name in CARD_NAMES.items():
        Card.objects.filter(image_path=image_path).update(name=name)


def restore_english_names(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for image_path, name in ENGLISH_NAMES.items():
        Card.objects.filter(image_path=image_path).update(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_seed_cards'),
    ]

    operations = [
        migrations.RunPython(localize_names, restore_english_names),
    ]
