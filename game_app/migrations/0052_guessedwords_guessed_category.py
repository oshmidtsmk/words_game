# Generated by Django 3.2.21 on 2024-02-18 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0051_remove_profile_number_of_letter'),
    ]

    operations = [
        migrations.AddField(
            model_name='guessedwords',
            name='guessed_category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
