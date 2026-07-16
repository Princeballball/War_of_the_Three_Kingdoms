import random
import string

from django.conf import settings
from django.db import models


class Room(models.Model):
    class RoomType(models.TextChoices):
        PUBLIC = 'public', '公開房'
        PRIVATE = 'private', '私人房'

    class Status(models.TextChoices):
        WAITING = 'waiting', '等待中'
        PLAYING = 'playing', '遊戲中'

    code = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=80)
    room_type = models.CharField(max_length=12, choices=RoomType.choices, default=RoomType.PUBLIC)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.WAITING)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_rooms',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)

    max_players = 5

    class Meta:
        ordering = ['status', '-created_at']

    def __str__(self):
        return f'{self.name} #{self.code}'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    @classmethod
    def generate_unique_code(cls):
        alphabet = string.ascii_uppercase + string.digits
        while True:
            code = ''.join(random.choices(alphabet, k=6))
            if not cls.objects.filter(code=code).exists():
                return code

    @property
    def player_count(self):
        return self.memberships.count()

    @property
    def is_full(self):
        return self.player_count >= self.max_players


class RoomMembership(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='room_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')
        ordering = ['joined_at']

    def __str__(self):
        return f'{self.user} in {self.room}'
