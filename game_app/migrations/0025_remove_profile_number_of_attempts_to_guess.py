# Generated by Django 3.2.21 on 2023-12-06 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0024_remove_profile_words'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='number_of_attempts_to_guess',
        ),
    ]