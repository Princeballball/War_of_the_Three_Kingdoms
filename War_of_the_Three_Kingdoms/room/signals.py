from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Room, RoomMembership


@receiver(post_delete, sender=RoomMembership)
def delete_room_without_players(sender, instance, **kwargs):
    if not RoomMembership.objects.filter(room_id=instance.room_id).exists():
        Room.objects.filter(pk=instance.room_id).delete()
