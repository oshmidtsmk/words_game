# Generated by Django 3.2.21 on 2023-11-23 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0020_alter_word_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='user',
        ),
        migrations.AddField(
            model_name='profile',
            name='words',
            field=models.ManyToManyField(to='game_app.Word'),
        ),
    ]
