from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(editable=False, max_length=6, unique=True)),
                ('name', models.CharField(max_length=80)),
                ('room_type', models.CharField(choices=[('public', '公開房'), ('private', '私人房')], default='public', max_length=12)),
                ('status', models.CharField(choices=[('waiting', '等待中'), ('playing', '遊戲中')], default='waiting', max_length=12)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rooms', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['status', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RoomMembership',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_at', models.DateTimeField(auto_now_add=True)),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memberships', to='room.room')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room_memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['joined_at'],
                'unique_together': {('room', 'user')},
            },
        ),
    ]
