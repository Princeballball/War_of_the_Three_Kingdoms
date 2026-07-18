from django.db import transaction
from django.utils import timezone

from .models import Room, RoomMembership


def join_room(room, user):
    with transaction.atomic():
        room = Room.objects.select_for_update().get(pk=room.pk)
        if room.status != Room.Status.WAITING:
            return room, False, '房間已經開始遊戲。'
        if room.memberships.count() >= room.max_players:
            return room, False, '房間已滿。'

        _, created = RoomMembership.objects.get_or_create(room=room, user=user)
        if not created:
            return room, False, '你已經在這個房間裡。'

        if room.memberships.count() >= room.max_players:
            room.status = Room.Status.PLAYING
            room.started_at = timezone.now()
            room.save(update_fields=['status', 'started_at'])
            from game.services import create_game_from_room

            create_game_from_room(room)
            return room, True, '房間已湊齊 5 人，自動開局。'

        return room, True, f'已加入房間，目前 {room.memberships.count()} / {room.max_players} 人。'


def leave_room(room, user):
    with transaction.atomic():
        room = Room.objects.select_for_update().get(pk=room.pk)
        RoomMembership.objects.filter(room=room, user=user).delete()
        return not Room.objects.filter(pk=room.pk).exists()


def join_auto_room(user):
    with transaction.atomic():
        room = (
            Room.objects.select_for_update()
            .filter(status=Room.Status.WAITING, room_type=Room.RoomType.PUBLIC, name='系統自動配對')
            .order_by('created_at')
            .first()
        )
        if room is None or room.memberships.count() >= room.max_players:
            room = Room.objects.create(name='系統自動配對', room_type=Room.RoomType.PUBLIC)

    return join_room(room, user)
