# Generated by Django 3.2.21 on 2023-11-24 06:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0023_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='words',
        ),
    ]
