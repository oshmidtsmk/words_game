# Generated by Django 3.2.21 on 2024-03-17 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0064_alter_profile_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='rating',
            field=models.CharField(blank=True, default='Поки що ви на останньому місці', max_length=100, null=True),
        ),
    ]
