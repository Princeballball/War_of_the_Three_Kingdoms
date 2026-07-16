from django.db import migrations, models


CARD_DETAILS = {
    'images/card/Wei/Cao_Cao.png': {
        'name': '曹操',
        'health': 4,
        'skills': [
            {'name': '奸雄', 'description': '每當你受到傷害後，你可以獲得對你造成傷害的牌。'},
            {'name': '護駕', 'description': '主公技。當你需要使用或打出【殺】時，你可以令其他魏勢力角色選擇是否幫你打出一張【殺】。'},
        ],
    },
    'images/card/Wei/Sima_Yi.png': {
        'name': '司馬懿',
        'health': 3,
        'skills': [
            {'name': '反饋', 'description': '每當你受到傷害後，你可以獲得傷害來源的一張牌。'},
            {'name': '鬼才', 'description': '在任意角色的判定牌生效前，你可以打出一張手牌代替之。'},
        ],
    },
    'images/card/Wei/Xiahou_Dun.png': {
        'name': '夏侯惇',
        'health': 4,
        'skills': [
            {'name': '剛烈', 'description': '每當你受到傷害後，你可以進行一次判定，若結果不為紅桃，傷害來源必須選擇一項：棄置兩張手牌，或受到你對其造成的 1 點傷害。'},
        ],
    },
    'images/card/Wei/Zhang_Liao.png': {
        'name': '張遼',
        'health': 4,
        'skills': [
            {'name': '突襲', 'description': '摸牌階段，你可以放棄摸牌，改為獲得最多兩名其他角色的各一張手牌。'},
        ],
    },
    'images/card/Wei/Xu_Chu.png': {
        'name': '許褚',
        'health': 4,
        'skills': [
            {'name': '裸衣', 'description': '摸牌階段，你可以少摸一張牌。若如此做，你本回合使用【殺】或【決鬥】造成的傷害 +1。'},
        ],
    },
    'images/card/Wei/Guo_Jia.png': {
        'name': '郭嘉',
        'health': 3,
        'skills': [
            {'name': '天妒', 'description': '在你的判定牌生效後，你可以獲得此判定牌。'},
            {'name': '遺計', 'description': '每當你受到 1 點傷害後，你可以觀看牌堆頂的兩張牌，然後將它們交給任意角色。'},
        ],
    },
    'images/card/Wei/Zhen_Ji.png': {
        'name': '甄姬',
        'health': 3,
        'skills': [
            {'name': '傾國', 'description': '你可以將一張黑色手牌當作【閃】使用或打出。'},
            {'name': '洛神', 'description': '準備階段，你可以進行一次判定，若判定結果為黑色，你獲得此牌且可重複此流程，直到判定結果為紅色。'},
        ],
    },
    'images/card/Shu/Liu_Bei.png': {
        'name': '劉備',
        'health': 4,
        'skills': [
            {'name': '仁德', 'description': '出牌階段，你可以將任意數量手牌分配給其他角色。若你分配的手牌不少於兩張，你回復 1 點體力。'},
            {'name': '激將', 'description': '主公技。當你需要使用或打出【殺】時，你可以令其他蜀勢力角色選擇是否幫你打出一張【殺】。'},
        ],
    },
    'images/card/Shu/Guan_Yu.png': {
        'name': '關羽',
        'health': 4,
        'skills': [
            {'name': '武聖', 'description': '你可以將一張紅色牌當作【殺】使用或打出。'},
        ],
    },
    'images/card/Shu/Zhang_Fei.png': {
        'name': '張飛',
        'health': 4,
        'skills': [
            {'name': '咆哮', 'description': '鎖定技，你使用【殺】無次數限制。'},
        ],
    },
    'images/card/Shu/Zhuge_Liang.png': {
        'name': '諸葛亮',
        'health': 3,
        'skills': [
            {'name': '觀星', 'description': '準備階段，你可以觀看牌堆頂的五張牌（若存活人數小於 4 則為存活人數），然後以任意順序放回牌堆頂或牌堆底。'},
            {'name': '空城', 'description': '鎖定技，若你沒有手牌，你不能成為【殺】或【決鬥】的目標。'},
        ],
    },
    'images/card/Shu/Zhao_Yun.png': {
        'name': '趙雲',
        'health': 4,
        'skills': [
            {'name': '龍膽', 'description': '你可以將【殺】當作【閃】、或將【閃】當作【殺】使用或打出。'},
        ],
    },
    'images/card/Shu/Ma_Chao.png': {
        'name': '馬超',
        'health': 4,
        'skills': [
            {'name': '馬術', 'description': '鎖定技，你計算與其他角色的距離 -1。'},
            {'name': '鐵騎', 'description': '當你使用【殺】指定目標後，你可以進行一次判定。若結果為紅色，該【殺】不可被【閃】抵消。'},
        ],
    },
    'images/card/Shu/Huang_Yueying.png': {
        'name': '黃月英',
        'health': 3,
        'skills': [
            {'name': '集智', 'description': '每當你使用一張非延時類錦囊牌時，你可以摸一張牌。'},
            {'name': '奇才', 'description': '鎖定技，你使用錦囊牌無距離限制。'},
        ],
    },
    'images/card/Wu/Sun_Quan.png': {
        'name': '孫權',
        'health': 4,
        'skills': [
            {'name': '制衡', 'description': '出牌階段限一次，你可以棄置任意數量的牌，然後摸等量的牌。'},
            {'name': '救援', 'description': '主公技、鎖定技。當其他吳勢力角色對你使用【桃】時，回復的體力值 +1。'},
        ],
    },
    'images/card/Wu/Gan_Ning.png': {
        'name': '甘寧',
        'health': 4,
        'skills': [
            {'name': '奇襲', 'description': '你可以將一張黑色牌當作【過河拆橋】使用。'},
        ],
    },
    'images/card/Wu/Lu_Meng.png': {
        'name': '呂蒙',
        'health': 4,
        'skills': [
            {'name': '克己', 'description': '若你於出牌階段未曾使用或打出過【殺】，你可以跳過棄牌階段。'},
        ],
    },
    'images/card/Wu/Huang_Gai.png': {
        'name': '黃蓋',
        'health': 4,
        'skills': [
            {'name': '苦肉', 'description': '出牌階段，你可以流失 1 點體力，然後摸兩張牌。'},
        ],
    },
    'images/card/Wu/Zhou_Yu.png': {
        'name': '周瑜',
        'health': 3,
        'skills': [
            {'name': '英姿', 'description': '摸牌階段，你可以多摸一張牌。'},
            {'name': '反間', 'description': '出牌階段限一次，你可以選擇一名角色並展示一張手牌，該角色選擇一種花色並獲得該牌。若花色不符，你對其造成 1 點傷害。'},
        ],
    },
    'images/card/Wu/Da_Qiao.png': {
        'name': '大喬',
        'health': 3,
        'skills': [
            {'name': '國色', 'description': '你可以將一張方塊牌當作【樂不思蜀】使用。'},
            {'name': '流離', 'description': '當你成為【殺】的目標時，你可以棄置一張牌，將此【殺】轉移給攻擊範圍內的另一名角色（不能是此【殺】的來源）。'},
        ],
    },
    'images/card/Wu/Lu_Xun.png': {
        'name': '陸遜',
        'health': 3,
        'skills': [
            {'name': '謙遜', 'description': '鎖定技，你不能成為【順手牽羊】和【兵糧寸斷】的目標。'},
            {'name': '連營', 'description': '每當你失去最後一張手牌後，你可以摸一張牌。'},
        ],
    },
    'images/card/Wu/Sun_Shangxiang.png': {
        'name': '孫尚香',
        'health': 3,
        'skills': [
            {'name': '結姻', 'description': '出牌階段限一次，你可以棄置兩張手牌並選擇一名受傷的男性角色，你與其各回復 1 點體力。'},
            {'name': '梟姬', 'description': '每當你失去一張裝備區裡的牌後，你可以摸兩張牌。'},
        ],
    },
    'images/card/Chun/Hua_Tuo.png': {
        'name': '華佗',
        'health': 3,
        'skills': [
            {'name': '急救', 'description': '你的回合外，你可以將一張紅色牌當作【桃】使用。'},
            {'name': '青囊', 'description': '出牌階段限一次，你可以棄置一張手牌並指定一名受傷角色，令其回復 1 點體力。'},
        ],
    },
    'images/card/Chun/Lu_Bu.png': {
        'name': '呂布',
        'health': 4,
        'skills': [
            {'name': '無雙', 'description': '鎖定技，你使用的【殺】需兩張【閃】才能抵消；你與他人【決鬥】時，對手每次需打出兩張【殺】。'},
        ],
    },
    'images/card/Chun/Diao_Chan.png': {
        'name': '貂蟬',
        'health': 3,
        'skills': [
            {'name': '離間', 'description': '出牌階段限一次，你可以棄置一張牌，令兩名男性角色進行【決鬥】（你決定誰先出【殺】）。'},
            {'name': '閉月', 'description': '結束階段，你可以摸一張牌。'},
        ],
    },
    'images/card/Chun/Hua_Xiong.png': {
        'name': '華雄',
        'health': 6,
        'skills': [
            {'name': '耀武', 'description': '鎖定技，每當你受到【殺】造成的傷害時，若此【殺】為紅色，傷害來源摸一張牌或回復 1 點體力。'},
        ],
    },
    'images/card/Chun/Yuan_Shu.png': {
        'name': '袁術',
        'health': 4,
        'skills': [
            {'name': '妄尊', 'description': '主公的準備階段，你可以摸一張牌，然後主公本回合手牌上限 -1。'},
            {'name': '同疾', 'description': '鎖定技，若你的手牌數大於你的體力值，其他角色對你使用【殺】時，若其攻擊範圍內有其他目標，其必須將目標改為其中之一。'},
        ],
    },
}


def seed_card_details(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    for image_path, details in CARD_DETAILS.items():
        Card.objects.filter(image_path=image_path).update(
            name=details['name'],
            health=details['health'],
            skills=details['skills'],
        )


def clear_card_details(apps, schema_editor):
    Card = apps.get_model('card', 'Card')
    Card.objects.filter(image_path__in=CARD_DETAILS).update(health=4, skills=[])


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0003_localize_card_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='health',
            field=models.PositiveSmallIntegerField(default=4),
        ),
        migrations.AddField(
            model_name='card',
            name='skills',
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.RunPython(seed_card_details, clear_card_details),
    ]
