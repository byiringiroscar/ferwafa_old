# Generated by Django 4.0.2 on 2022-03-10 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_alter_legend_story_legend_inspiring_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='live_match',
            name='team1_logo',
            field=models.ImageField(default='apr.png', upload_to='images/'),
        ),
        migrations.AddField(
            model_name='live_match',
            name='team2_logo',
            field=models.ImageField(default='rayon.png', upload_to='images/'),
        ),
    ]