# Generated by Django 3.2.21 on 2023-10-27 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0003_auto_20231027_1123'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='failure',
            field=models.CharField(default='Try again...', max_length=100),
        ),
        migrations.AddField(
            model_name='word',
            name='success',
            field=models.CharField(default='You have guessed it!', max_length=100),
        ),
    ]