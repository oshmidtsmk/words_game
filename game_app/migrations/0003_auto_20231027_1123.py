# Generated by Django 3.2.21 on 2023-10-27 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0002_word_masked_word'),
    ]

    operations = [
        migrations.AddField(
            model_name='word',
            name='letter',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='word',
            name='number_of_letter',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
