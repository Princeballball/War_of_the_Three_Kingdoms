from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_game_phase_game_has_drawn_game_turn_number_gamecard'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='slash_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamecard',
            name='equipment_slot',
            field=models.CharField(blank=True, choices=[('', '無'), ('weapon', '武器'), ('armor', '防具'), ('attack_horse', '進攻馬'), ('defense_horse', '防禦馬')], default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='game',
            name='phase',
            field=models.CharField(choices=[('start', '準備階段'), ('judgment', '判定階段'), ('draw', '摸牌階段'), ('play', '出牌階段'), ('discard', '棄牌階段'), ('end', '結束階段')], default='start', max_length=12),
        ),
    ]
