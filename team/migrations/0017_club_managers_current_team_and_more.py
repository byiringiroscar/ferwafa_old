# Generated by Django 4.0.2 on 2022-05-12 10:22

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0016_connect_message_connect_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='club_managers',
            name='current_team',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='team.table_ranking'),
        ),
        migrations.AlterField(
            model_name='club_managers',
            name='managers_birth_date',
            field=models.DateField(default=datetime.date(2022, 5, 12)),
        ),
        migrations.AlterField(
            model_name='connect_message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 10, 22, 2, 19937, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='player_profile',
            name='player_born',
            field=models.DateTimeField(blank=True, default=datetime.date(2022, 5, 12), null=True),
        ),
    ]
