from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_game_slash_count_gamecard_equipment_slot_phase_choices'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='pending_action',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='gamecard',
            name='zone',
            field=models.CharField(choices=[('deck', '牌堆'), ('hand', '手牌'), ('discard', '棄牌堆'), ('equipment', '裝備區'), ('judgment', '判定區')], default='deck', max_length=12),
        ),
    ]
