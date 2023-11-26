# Generated by Django 3.2.21 on 2023-11-21 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0017_auto_20231119_1513'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='words',
        ),
        migrations.AddField(
            model_name='word',
            name='profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='words', to='game_app.profile'),
        ),
    ]
