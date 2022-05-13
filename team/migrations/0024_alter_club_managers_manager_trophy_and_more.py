# Generated by Django 4.0.2 on 2022-05-13 10:25

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0023_trophy_manager_alter_connect_message_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club_managers',
            name='manager_trophy',
            field=models.ManyToManyField(blank=True, null=True, to='team.Trophy_manager'),
        ),
        migrations.AlterField(
            model_name='club_managers',
            name='managers_birth_date',
            field=models.DateField(default=datetime.date(2022, 5, 13)),
        ),
        migrations.AlterField(
            model_name='connect_message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 13, 10, 25, 0, 255517, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='player_profile',
            name='player_born',
            field=models.DateTimeField(blank=True, default=datetime.date(2022, 5, 13), null=True),
        ),
    ]
