# Generated by Django 3.2.21 on 2023-11-26 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0029_profile_masked_word'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='masked_word',
            new_name='profile',
        ),
    ]
