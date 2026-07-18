import random

from django.db import transaction
from django.utils import timezone

from card.models import Card

from .models import Game, GameCard, GamePlayer


IDENTITY_NAMES = ['主公', '忠臣', '反賊', '反賊', '內奸']
GENERAL_FACTIONS = [Card.Faction.WEI, Card.Faction.SHU, Card.Faction.WU, Card.Faction.CHUN]
WEAPON_CARDS = {
    '諸葛連弩',
    '青釭劍',
    '雌雄雙股劍',
    '寒冰劍',
    '青龍偃月刀',
    '丈八蛇矛',
    '貫石斧',
    '方天畫戟',
    '麒麟弓',
}
ARMOR_CARDS = {'八卦陣', '仁王盾'}
WEAPON_RANGES = {
    '諸葛連弩': 1,
    '青釭劍': 2,
    '雌雄雙股劍': 2,
    '寒冰劍': 2,
    '青龍偃月刀': 3,
    '丈八蛇矛': 3,
    '貫石斧': 3,
    '方天畫戟': 4,
    '麒麟弓': 5,
}
DELAYED_TRICKS = {'樂不思蜀', '閃電'}


def assign_missing_general_candidates(game):
    general_cards = list(Card.objects.filter(faction__in=GENERAL_FACTIONS))
    if len(general_cards) < 3:
        return

    used_candidate_ids = set(
        GamePlayer.general_candidates.through.objects
        .filter(gameplayer__game=game)
        .values_list('card_id', flat=True)
    )
    available_cards = [card for card in general_cards if card.id not in used_candidate_ids]
    if len(available_cards) < 3:
        available_cards = general_cards[:]
    random.shuffle(available_cards)

    for player in game.players.order_by('seat_order'):
        if player.general_candidates.exists() or player.selected_general_id:
            continue
        if len(available_cards) < 3:
            available_cards = general_cards[:]
            random.shuffle(available_cards)
        player.general_candidates.set(available_cards[:3])
        available_cards = available_cards[3:]


def create_game_from_room(room):
    with transaction.atomic():
        game, created = Game.objects.get_or_create(room=room)
        if not created and game.players.exists():
            return game

        memberships = list(room.memberships.select_related('user').order_by('joined_at'))
        if len(memberships) != room.max_players:
            return game

        identity_cards = {
            card.name: card
            for card in Card.objects.filter(faction=Card.Faction.IDENTITY, name__in=set(IDENTITY_NAMES))
        }
        identities = IDENTITY_NAMES[:]
        random.shuffle(identities)

        GamePlayer.objects.filter(game=game).delete()
        general_cards = list(Card.objects.filter(faction__in=GENERAL_FACTIONS))
        random.shuffle(general_cards)

        for seat_order, membership in enumerate(memberships, start=1):
            identity_name = identities[seat_order - 1]
            player = GamePlayer.objects.create(
                game=game,
                user=membership.user,
                seat_order=seat_order,
                identity_card=identity_cards.get(identity_name),
            )
            start_index = (seat_order - 1) * 3
            player.general_candidates.set(general_cards[start_index:start_index + 3])

        lord = game.players.filter(identity_card__name='主公').select_related('user').first()
        if lord:
            game.current_turn = lord.user
            game.save(update_fields=['current_turn'])

        return game


def choose_general(game_player, general):
    with transaction.atomic():
        game_player = (
            GamePlayer.objects
            .select_for_update()
            .select_related('game')
            .prefetch_related('general_candidates')
            .get(pk=game_player.pk)
        )
        if game_player.selected_general_id:
            return game_player, False, '你已經選過武將。'
        if not game_player.general_candidates.filter(pk=general.pk).exists():
            return game_player, False, '這張武將不在你的候選列表中。'

        game_player.selected_general = general
        bonus_health = 1 if game_player.identity_card and game_player.identity_card.name == '主公' else 0
        game_player.max_health = (general.health or 4) + bonus_health
        game_player.current_health = game_player.max_health
        game_player.save(update_fields=['selected_general', 'max_health', 'current_health'])

        game = game_player.game
        if not game.players.filter(selected_general__isnull=True).exists():
            start_game(game)

        return game_player, True, f'你選擇了 {general.name}。'


def start_game(game):
    game = Game.objects.select_for_update().get(pk=game.pk)
    if game.game_cards.exists():
        return game

    cards = []
    playable_cards = Card.objects.filter(faction__in=[Card.Faction.BASIC, Card.Faction.FUNCTION, Card.Faction.EQUIPMENT], deck_count__gt=0)
    for card in playable_cards:
        cards.extend([card] * card.deck_count)
    random.shuffle(cards)

    GameCard.objects.bulk_create([
        GameCard(game=game, card=card, zone=GameCard.Zone.DECK, position=index)
        for index, card in enumerate(cards, start=1)
    ])

    for player in game.players.order_by('seat_order'):
        draw_cards(game, player, 4)

    game.status = Game.Status.PLAYING
    game.phase = Game.Phase.DRAW
    game.has_drawn = False
    game.slash_count = 0
    game.started_at = timezone.now()
    game.save(update_fields=['status', 'phase', 'has_drawn', 'slash_count', 'started_at'])
    return game


def draw_cards(game, player, amount=2):
    drawn_cards = []
    for _ in range(amount):
        top_card = game.game_cards.filter(zone=GameCard.Zone.DECK).order_by('position', 'id').first()
        if top_card is None:
            break
        top_card.owner = player
        top_card.zone = GameCard.Zone.HAND
        top_card.position = player.cards.filter(zone=GameCard.Zone.HAND).count() + 1
        top_card.save(update_fields=['owner', 'zone', 'position'])
        drawn_cards.append(top_card)
    return drawn_cards


def move_to_discard(game_card):
    game = game_card.game
    game_card.owner = None
    game_card.zone = GameCard.Zone.DISCARD
    game_card.equipment_slot = ''
    game_card.position = game.game_cards.filter(zone=GameCard.Zone.DISCARD).count() + 1
    game_card.save(update_fields=['owner', 'zone', 'equipment_slot', 'position'])


def first_hand_card(player, name):
    return player.cards.filter(zone=GameCard.Zone.HAND, card__name=name).order_by('position', 'id').first()


def consume_hand_card(game_card):
    move_to_discard(game_card)


def attack_range(player):
    weapon = player.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=GameCard.EquipmentSlot.WEAPON).select_related('card').first()
    return WEAPON_RANGES.get(weapon.card.name, 1) if weapon else 1


def seat_distance(source, target):
    players = list(source.game.players.filter(is_alive=True).order_by('seat_order'))
    source_index = players.index(source)
    target_index = players.index(target)
    distance = abs(source_index - target_index)
    physical = min(distance, len(players) - distance)
    attack_horse = 1 if source.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=GameCard.EquipmentSlot.ATTACK_HORSE).exists() else 0
    defense_horse = 1 if target.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=GameCard.EquipmentSlot.DEFENSE_HORSE).exists() else 0
    return max(1, physical + defense_horse - attack_horse)


def check_game_over(game):
    alive_players = game.players.filter(is_alive=True).select_related('identity_card')
    lord_alive = alive_players.filter(identity_card__name='主公').exists()
    rebel_count = alive_players.filter(identity_card__name='反賊').count()
    traitor_count = alive_players.filter(identity_card__name='內奸').count()
    loyal_count = alive_players.filter(identity_card__name='忠臣').count()

    winner = ''
    if not lord_alive:
        winner = '內奸獲勝' if rebel_count == 0 and loyal_count == 0 and traitor_count == 1 else '反賊獲勝'
    elif rebel_count == 0 and traitor_count == 0:
        winner = '主公與忠臣獲勝'

    if winner:
        game.status = Game.Status.FINISHED
        game.pending_action = {}
        game.save(update_fields=['status', 'pending_action'])
    return winner


def kill_player(game, target, source=None):
    target.is_alive = False
    target.current_health = 0
    target.save(update_fields=['is_alive', 'current_health'])

    messages = [f'{target.user.username} 死亡。']
    if source and target.identity_card and target.identity_card.name == '反賊':
        draw_cards(game, source, 3)
        messages.append(f'{source.user.username} 擊殺反賊，摸 3 張牌。')
    if (
        source
        and target.identity_card
        and source.identity_card
        and target.identity_card.name == '忠臣'
        and source.identity_card.name == '主公'
    ):
        for card in list(source.cards.filter(zone__in=[GameCard.Zone.HAND, GameCard.Zone.EQUIPMENT])):
            move_to_discard(card)
        messages.append('主公誤殺忠臣，棄置所有手牌與裝備。')

    winner = check_game_over(game)
    if winner:
        messages.append(winner)
    return messages


def apply_damage(game, target, amount=1, source=None):
    target.current_health -= amount
    target.save(update_fields=['current_health'])
    if target.current_health <= 0:
        game.pending_action = {
            'type': 'dying',
            'target_id': target.id,
            'source_id': source.id if source else None,
            'message': f'{target.user.username} 瀕死，需要【桃】。',
        }
        game.save(update_fields=['pending_action'])
        return f'{target.user.username} 進入瀕死狀態。'
    return f'{target.user.username} 受到 {amount} 點傷害。'


def resolve_judgment(game, player):
    messages = []
    delayed_cards = list(player.cards.filter(zone=GameCard.Zone.JUDGMENT).select_related('card').order_by('-position', '-id'))
    for delayed_card in delayed_cards:
        judgment_card = game.game_cards.filter(zone=GameCard.Zone.DECK).order_by('position', 'id').first()
        judgment_hit = random.choice([True, False])
        if judgment_card:
            move_to_discard(judgment_card)

        if delayed_card.card.name == '樂不思蜀':
            if judgment_hit:
                game.phase = Game.Phase.DISCARD
                messages.append(f'{player.user.username} 的【樂不思蜀】判定未通過，跳過出牌階段。')
            else:
                messages.append(f'{player.user.username} 的【樂不思蜀】判定通過。')
            move_to_discard(delayed_card)
        elif delayed_card.card.name == '閃電':
            if judgment_hit:
                messages.append(apply_damage(game, player, 3))
                move_to_discard(delayed_card)
            else:
                next_player = next_alive_player(game, player)
                delayed_card.owner = next_player
                delayed_card.position = next_player.cards.filter(zone=GameCard.Zone.JUDGMENT).count() + 1
                delayed_card.save(update_fields=['owner', 'position'])
                messages.append(f'【閃電】判定未命中，傳給 {next_player.user.username}。')
    return messages


def next_alive_player(game, player):
    players = list(game.players.filter(is_alive=True).order_by('seat_order'))
    current_index = next((index for index, item in enumerate(players) if item.pk == player.pk), 0)
    return players[(current_index + 1) % len(players)]


def draw_for_turn(game, player):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(pk=game.pk)
        if game.status != Game.Status.PLAYING:
            return False, '遊戲尚未開始。'
        if game.current_turn_id != player.user_id:
            return False, '還沒輪到你。'
        if game.has_drawn:
            return False, '你本回合已經摸過牌。'
        messages = resolve_judgment(game, player)
        if game.pending_action:
            return False, '請先處理待回應事件。'
        if game.phase == Game.Phase.DISCARD:
            game.has_drawn = True
            game.save(update_fields=['has_drawn'])
            return True, '；'.join(messages) or '你跳過出牌階段。'
        draw_cards(game, player, 2)
        game.phase = Game.Phase.PLAY
        game.has_drawn = True
        game.save(update_fields=['phase', 'has_drawn'])
        return True, '你摸了 2 張牌。'


def discard_excess_cards(game, player):
    hand_limit = player.current_health
    hand_cards = list(player.cards.filter(zone=GameCard.Zone.HAND).order_by('-position', '-id'))
    excess = max(len(hand_cards) - hand_limit, 0)
    for game_card in hand_cards[:excess]:
        game_card.owner = None
        game_card.zone = GameCard.Zone.DISCARD
        game_card.position = game.game_cards.filter(zone=GameCard.Zone.DISCARD).count() + 1
        game_card.equipment_slot = ''
        game_card.save(update_fields=['owner', 'zone', 'position', 'equipment_slot'])
    return excess


def end_turn(game, player):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(pk=game.pk)
        if game.status != Game.Status.PLAYING:
            return False, '遊戲尚未開始。'
        if game.current_turn_id != player.user_id:
            return False, '還沒輪到你。'
        if game.pending_action:
            return False, '請先處理待回應事件。'

        discarded = discard_excess_cards(game, player)
        next_player = next_alive_player(game, player)
        game.current_turn = next_player.user
        game.turn_number += 1
        game.phase = Game.Phase.START
        game.has_drawn = False
        game.slash_count = 0
        game.save(update_fields=['current_turn', 'turn_number', 'phase', 'has_drawn', 'slash_count'])
        suffix = f'，自動棄置 {discarded} 張超出手牌上限的牌' if discarded else ''
        return True, f'回合結束{suffix}，輪到 {next_player.user.username}。'


def equipment_slot_for(card):
    if card.name in WEAPON_CARDS:
        return GameCard.EquipmentSlot.WEAPON
    if card.name in ARMOR_CARDS:
        return GameCard.EquipmentSlot.ARMOR
    if card.name == '進攻馬':
        return GameCard.EquipmentSlot.ATTACK_HORSE
    if card.name == '防禦馬':
        return GameCard.EquipmentSlot.DEFENSE_HORSE
    return ''


def use_hand_card(game, player, game_card, target_player_id=None):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(pk=game.pk)
        player = GamePlayer.objects.select_for_update().get(pk=player.pk)
        game_card = GameCard.objects.select_for_update().select_related('card').get(pk=game_card.pk)

        if game.status != Game.Status.PLAYING:
            return False, '遊戲尚未開始。'
        if game.current_turn_id != player.user_id:
            return False, '還沒輪到你。'
        if game_card.owner_id != player.pk or game_card.zone != GameCard.Zone.HAND:
            return False, '這張牌不在你的手牌中。'

        card = game_card.card
        message = f'你使用了 {card.name}。'

        def damage(target, amount=1):
            return apply_damage(game, target, amount, player)

        def heal(target, amount=1):
            target.current_health = min(target.current_health + amount, target.max_health)
            target.save(update_fields=['current_health'])

        def discard_random_from(target):
            target_card = (
                target.cards
                .filter(zone__in=[GameCard.Zone.HAND, GameCard.Zone.EQUIPMENT])
                .order_by('?')
                .first()
            )
            if target_card:
                target_card.owner = None
                target_card.zone = GameCard.Zone.DISCARD
                target_card.position = game.game_cards.filter(zone=GameCard.Zone.DISCARD).count() + 1
                target_card.save(update_fields=['owner', 'zone', 'position'])
            return target_card

        def steal_random_from(target):
            target_card = target.cards.filter(zone=GameCard.Zone.HAND).order_by('?').first()
            if target_card:
                target_card.owner = player
                target_card.position = player.cards.filter(zone=GameCard.Zone.HAND).count() + 1
                target_card.save(update_fields=['owner', 'position'])
            return target_card

        if card.name == '殺':
            has_crossbow = player.cards.filter(zone=GameCard.Zone.EQUIPMENT, card__name='諸葛連弩').exists()
            if game.slash_count >= 1 and not has_crossbow:
                return False, '你本回合已經使用過【殺】。'
            target = GamePlayer.objects.select_for_update().filter(pk=target_player_id, game=game, is_alive=True).first()
            if target is None or target.pk == player.pk:
                return False, '請選擇一名有效目標。'
            if seat_distance(player, target) > attack_range(player):
                return False, '目標超出攻擊範圍。'
            game.slash_count += 1
            game.save(update_fields=['slash_count'])
            armor = target.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=GameCard.EquipmentSlot.ARMOR).select_related('card').first()
            weapon = player.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=GameCard.EquipmentSlot.WEAPON).select_related('card').first()
            if armor and armor.card.name == '仁王盾' and not (weapon and weapon.card.name == '青釭劍'):
                message = f'{target.user.username} 的【仁王盾】抵消了【殺】。'
            elif first_hand_card(target, '閃'):
                game.pending_action = {
                    'type': 'slash_response',
                    'source_id': player.id,
                    'target_id': target.id,
                    'card_id': game_card.id,
                    'message': f'{target.user.username} 需要打出【閃】抵消【殺】。',
                }
                game.save(update_fields=['pending_action'])
                return True, game.pending_action['message']
            elif armor and armor.card.name == '八卦陣' and not (weapon and weapon.card.name == '青釭劍') and random.choice([True, False]):
                message = f'{target.user.username} 的【八卦陣】判定成功，視為打出【閃】。'
            else:
                damage_message = damage(target)
                message = f'你對 {target.user.username} 使用【殺】。{damage_message}'
                if weapon and weapon.card.name == '麒麟弓':
                    horse = target.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot__in=[GameCard.EquipmentSlot.ATTACK_HORSE, GameCard.EquipmentSlot.DEFENSE_HORSE]).first()
                    if horse:
                        move_to_discard(horse)
                        message += ' 麒麟弓棄置了目標的一匹馬。'
        elif card.name == '桃':
            if player.current_health < player.max_health:
                heal(player)
                message = '你使用【桃】回復 1 點體力。'
            else:
                return False, '你目前是滿體力，不能使用【桃】。'
        elif card.name == '無中生有':
            draw_cards(game, player, 2)
            message = '你使用【無中生有】，摸了 2 張牌。'
        elif card.name == '桃園結義':
            healed = 0
            for target in game.players.filter(is_alive=True):
                if target.current_health < target.max_health:
                    heal(target)
                    healed += 1
            message = f'你使用【桃園結義】，{healed} 名角色回復 1 點體力。'
        elif card.name in ['南蠻入侵', '萬箭齊發']:
            targets = game.players.select_for_update().filter(is_alive=True).exclude(pk=player.pk)
            for target in targets:
                required = '殺' if card.name == '南蠻入侵' else '閃'
                response_card = first_hand_card(target, required)
                if response_card:
                    consume_hand_card(response_card)
                else:
                    damage(target)
            message = f'你使用【{card.name}】，所有其他角色各受到 1 點傷害。'
        elif card.name == '決鬥':
            target = GamePlayer.objects.select_for_update().filter(pk=target_player_id, game=game, is_alive=True).first()
            if target is None or target.pk == player.pk:
                return False, '請選擇一名有效目標。'
            target_kill = first_hand_card(target, '殺')
            player_kill = first_hand_card(player, '殺')
            if target_kill:
                consume_hand_card(target_kill)
                if player_kill:
                    consume_hand_card(player_kill)
                    damage_message = damage(target)
                    message = f'雙方打出【殺】後，{target.user.username} 未能繼續，{damage_message}'
                else:
                    damage_message = damage(player)
                    message = f'{target.user.username} 打出【殺】，你未能回應，{damage_message}'
            else:
                damage_message = damage(target)
                message = f'{target.user.username} 未打出【殺】，{damage_message}'
        elif card.name == '過河拆橋':
            target = GamePlayer.objects.select_for_update().filter(pk=target_player_id, game=game, is_alive=True).first()
            if target is None or target.pk == player.pk:
                return False, '請選擇一名有效目標。'
            discarded = discard_random_from(target)
            message = f'你拆掉了 {target.user.username} 的一張牌。' if discarded else f'{target.user.username} 沒有可拆的牌。'
        elif card.name == '順手牽羊':
            target = GamePlayer.objects.select_for_update().filter(pk=target_player_id, game=game, is_alive=True).first()
            if target is None or target.pk == player.pk:
                return False, '請選擇一名有效目標。'
            if seat_distance(player, target) > 1:
                return False, '【順手牽羊】只能指定距離 1 以內的目標。'
            stolen = steal_random_from(target)
            message = f'你順走了 {target.user.username} 的一張手牌。' if stolen else f'{target.user.username} 沒有手牌可拿。'
        elif card.name == '五穀豐登':
            for target in game.players.filter(is_alive=True):
                draw_cards(game, target, 1)
            message = '你使用【五穀豐登】，每名存活角色摸 1 張牌。'
        elif card.name == '樂不思蜀':
            target = GamePlayer.objects.select_for_update().filter(pk=target_player_id, game=game, is_alive=True).first()
            if target is None or target.pk == player.pk:
                return False, '請選擇一名有效目標。'
            game_card.owner = target
            game_card.zone = GameCard.Zone.JUDGMENT
            game_card.position = target.cards.filter(zone=GameCard.Zone.JUDGMENT).count() + 1
            game_card.save(update_fields=['owner', 'zone', 'position'])
            return True, f'你將【樂不思蜀】放入 {target.user.username} 的判定區。'
        elif card.name == '閃電':
            game_card.zone = GameCard.Zone.JUDGMENT
            game_card.position = player.cards.filter(zone=GameCard.Zone.JUDGMENT).count() + 1
            game_card.save(update_fields=['zone', 'position'])
            return True, '你將【閃電】放入自己的判定區。'
        elif card.name in ['借刀殺人', '無懈可擊']:
            message = f'你使用【{card.name}】。目前此牌採簡化處理。'
        elif card.faction == Card.Faction.EQUIPMENT:
            slot = equipment_slot_for(card)
            if not slot:
                return False, '這張裝備牌尚未設定裝備槽。'
            old_equipment = player.cards.filter(zone=GameCard.Zone.EQUIPMENT, equipment_slot=slot).first()
            if old_equipment:
                old_equipment.owner = None
                old_equipment.zone = GameCard.Zone.DISCARD
                old_equipment.equipment_slot = ''
                old_equipment.position = game.game_cards.filter(zone=GameCard.Zone.DISCARD).count() + 1
                old_equipment.save(update_fields=['owner', 'zone', 'equipment_slot', 'position'])
            game_card.zone = GameCard.Zone.EQUIPMENT
            game_card.equipment_slot = slot
            game_card.position = player.cards.filter(zone=GameCard.Zone.EQUIPMENT).count() + 1
            game_card.save(update_fields=['zone', 'equipment_slot', 'position'])
            return True, f'你裝備了 {card.name}。'

        game_card.owner = None
        game_card.zone = GameCard.Zone.DISCARD
        game_card.position = game.game_cards.filter(zone=GameCard.Zone.DISCARD).count() + 1
        game_card.save(update_fields=['owner', 'zone', 'position'])
        return True, message


def respond_with_card(game, player, response):
    with transaction.atomic():
        game = Game.objects.select_for_update().get(pk=game.pk)
        player = GamePlayer.objects.select_for_update().get(pk=player.pk)
        pending = game.pending_action or {}
        if not pending:
            return False, '目前沒有需要回應的事件。'

        if pending.get('type') == 'slash_response':
            target_id = pending.get('target_id')
            source = GamePlayer.objects.filter(pk=pending.get('source_id'), game=game).first()
            target = GamePlayer.objects.select_for_update().filter(pk=target_id, game=game).first()
            slash_card = GameCard.objects.filter(pk=pending.get('card_id'), game=game).first()
            if player.pk != target_id:
                return False, '只有被【殺】指定的目標可以回應。'

            if response == 'dodge':
                dodge = first_hand_card(player, '閃')
                if dodge is None:
                    return False, '你沒有【閃】可以打出。'
                consume_hand_card(dodge)
                if slash_card:
                    move_to_discard(slash_card)
                game.pending_action = {}
                game.save(update_fields=['pending_action'])
                return True, '你打出【閃】，抵消了【殺】。'

            if slash_card:
                move_to_discard(slash_card)
            message = apply_damage(game, target, 1, source)
            if not game.pending_action or game.pending_action.get('type') != 'dying':
                game.pending_action = {}
                game.save(update_fields=['pending_action'])
            return True, f'你沒有打出【閃】。{message}'

        if pending.get('type') == 'dying':
            target = GamePlayer.objects.select_for_update().filter(pk=pending.get('target_id'), game=game).first()
            source = GamePlayer.objects.filter(pk=pending.get('source_id'), game=game).first()
            if response == 'peach':
                peach = first_hand_card(player, '桃')
                if peach is None:
                    return False, '你沒有【桃】可以打出。'
                consume_hand_card(peach)
                target.current_health += 1
                target.save(update_fields=['current_health'])
                if target.current_health > 0:
                    game.pending_action = {}
                    game.save(update_fields=['pending_action'])
                    return True, f'{player.user.username} 使用【桃】救回了 {target.user.username}。'
                return True, f'{player.user.username} 使用【桃】，但 {target.user.username} 仍在瀕死狀態。'

            messages = kill_player(game, target, source)
            game.pending_action = {}
            game.save(update_fields=['pending_action'])
            return True, ' '.join(messages)

        return False, '未知的待回應事件。'
