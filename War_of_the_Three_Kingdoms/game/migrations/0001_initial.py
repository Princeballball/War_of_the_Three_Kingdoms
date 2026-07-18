from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('card', '0007_add_equipment_cards'),
        ('room', '0002_alter_room_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('setup', '準備中'), ('playing', '遊戲中'), ('finished', '已結束')], default='setup', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('current_turn', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='current_games', to=settings.AUTH_USER_MODEL)),
                ('room', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='game', to='room.room')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='GamePlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seat_order', models.PositiveSmallIntegerField()),
                ('max_health', models.PositiveSmallIntegerField(default=4)),
                ('current_health', models.PositiveSmallIntegerField(default=4)),
                ('is_alive', models.BooleanField(default=True)),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='players', to='game.game')),
                ('identity_card', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='identity_game_players', to='card.card')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_players', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['seat_order'],
                'unique_together': {('game', 'user'), ('game', 'seat_order')},
            },
        ),
    ]
