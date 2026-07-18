from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0007_add_equipment_cards'),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameplayer',
            name='general_candidates',
            field=models.ManyToManyField(blank=True, related_name='candidate_game_players', to='card.card'),
        ),
        migrations.AddField(
            model_name='gameplayer',
            name='selected_general',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='selected_game_players', to='card.card'),
        ),
    ]
