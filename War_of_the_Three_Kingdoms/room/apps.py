from django.apps import AppConfig


class RoomConfig(AppConfig):
    name = 'room'

    def ready(self):
        import room.signals  # noqa: F401
