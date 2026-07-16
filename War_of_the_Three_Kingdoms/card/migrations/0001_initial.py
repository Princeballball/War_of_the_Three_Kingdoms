from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('faction', models.CharField(choices=[('Chun', '群'), ('Shu', '蜀'), ('Wei', '魏'), ('Wu', '吳')], max_length=12)),
                ('image_path', models.CharField(max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['faction', 'name'],
            },
        ),
    ]
