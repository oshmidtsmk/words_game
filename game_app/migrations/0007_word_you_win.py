# Generated by Django 3.2.21 on 2023-11-03 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0006_word_number_of_attempts'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='you_win',
            field=models.CharField(default='Congrats! You have GUESSED IT!!!!', max_length=100),
        ),
    ]
