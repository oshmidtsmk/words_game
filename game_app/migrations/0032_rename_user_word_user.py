# Generated by Django 3.2.21 on 2023-11-26 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0031_auto_20231126_0908'),
    ]

    operations = [
        migrations.RenameField(
            model_name='word',
            old_name='User',
            new_name='user',
        ),
    ]
