from django.db import models


class Card(models.Model):
    class Faction(models.TextChoices):
        CHUN = 'Chun', '群'
        SHU = 'Shu', '蜀'
        WEI = 'Wei', '魏'
        WU = 'Wu', '吳'
        IDENTITY = 'Identity', '身份'
        BASIC = 'Basic', '基本牌'
        FUNCTION = 'Function', '功能牌'
        EQUIPMENT = 'Equipment', '裝備牌'

    name = models.CharField(max_length=80)
    faction = models.CharField(max_length=16, choices=Faction.choices)
    health = models.PositiveSmallIntegerField(default=4)
    deck_count = models.PositiveSmallIntegerField(default=1)
    skills = models.JSONField(default=list, blank=True)
    image_path = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['faction', 'name']

    def __str__(self):
        return self.name

    @property
    def faction_label(self):
        return self.get_faction_display()
