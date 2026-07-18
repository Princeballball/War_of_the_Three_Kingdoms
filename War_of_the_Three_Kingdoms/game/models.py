from django.conf import settings
from django.db import models


class Game(models.Model):
    class Status(models.TextChoices):
        SETUP = 'setup', '準備中'
        PLAYING = 'playing', '遊戲中'
        FINISHED = 'finished', '已結束'

    class Phase(models.TextChoices):
        START = 'start', '準備階段'
        JUDGMENT = 'judgment', '判定階段'
        DRAW = 'draw', '摸牌階段'
        PLAY = 'play', '出牌階段'
        DISCARD = 'discard', '棄牌階段'
        END = 'end', '結束階段'

    room = models.OneToOneField('room.Room', on_delete=models.CASCADE, related_name='game')
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.SETUP)
    phase = models.CharField(max_length=12, choices=Phase.choices, default=Phase.START)
    turn_number = models.PositiveIntegerField(default=1)
    has_drawn = models.BooleanField(default=False)
    slash_count = models.PositiveSmallIntegerField(default=0)
    pending_action = models.JSONField(default=dict, blank=True)
    current_turn = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_games',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.room.name} #{self.room.code}'


class GamePlayer(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='game_players')
    seat_order = models.PositiveSmallIntegerField()
    identity_card = models.ForeignKey(
        'card.Card',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='identity_game_players',
    )
    general_candidates = models.ManyToManyField(
        'card.Card',
        blank=True,
        related_name='candidate_game_players',
    )
    selected_general = models.ForeignKey(
        'card.Card',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='selected_game_players',
    )
    max_health = models.PositiveSmallIntegerField(default=4)
    current_health = models.PositiveSmallIntegerField(default=4)
    is_alive = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['seat_order']
        unique_together = (('game', 'user'), ('game', 'seat_order'))

    def __str__(self):
        return f'{self.user} - {self.identity_card}'


class GameCard(models.Model):
    class Zone(models.TextChoices):
        DECK = 'deck', '牌堆'
        HAND = 'hand', '手牌'
        DISCARD = 'discard', '棄牌堆'
        EQUIPMENT = 'equipment', '裝備區'
        JUDGMENT = 'judgment', '判定區'

    class EquipmentSlot(models.TextChoices):
        NONE = '', '無'
        WEAPON = 'weapon', '武器'
        ARMOR = 'armor', '防具'
        ATTACK_HORSE = 'attack_horse', '進攻馬'
        DEFENSE_HORSE = 'defense_horse', '防禦馬'

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_cards')
    card = models.ForeignKey('card.Card', on_delete=models.CASCADE, related_name='game_cards')
    owner = models.ForeignKey(GamePlayer, on_delete=models.CASCADE, null=True, blank=True, related_name='cards')
    zone = models.CharField(max_length=12, choices=Zone.choices, default=Zone.DECK)
    equipment_slot = models.CharField(max_length=16, choices=EquipmentSlot.choices, blank=True, default='')
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['position', 'id']

    def __str__(self):
        return f'{self.card.name} - {self.get_zone_display()}'
