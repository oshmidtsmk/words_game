# Generated by Django 3.2.21 on 2024-03-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0057_alter_profile_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='default_profile_pic.png', upload_to='profile_pics/'),
        ),
    ]
