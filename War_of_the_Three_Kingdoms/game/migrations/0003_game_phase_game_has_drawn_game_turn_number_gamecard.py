from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_add_basic_cards'),
        ('game', '0002_gameplayer_general_candidates_and_selected_general'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='has_drawn',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='game',
            name='phase',
            field=models.CharField(choices=[('prepare', '準備階段'), ('draw', '摸牌階段'), ('play', '出牌階段'), ('discard', '棄牌階段')], default='prepare', max_length=12),
        ),
        migrations.AddField(
            model_name='game',
            name='turn_number',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.CreateModel(
            name='GameCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zone', models.CharField(choices=[('deck', '牌堆'), ('hand', '手牌'), ('discard', '棄牌堆'), ('equipment', '裝備區')], default='deck', max_length=12)),
                ('position', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('card', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_cards', to='card.card')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='game_cards', to='game.game')),
                ('owner', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cards', to='game.gameplayer')),
            ],
            options={
                'ordering': ['position', 'id'],
            },
        ),
    ]
