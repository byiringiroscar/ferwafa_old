# Generated by Django 4.0.2 on 2022-05-12 10:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0018_club_managers_current_season_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trophy_manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trophy_name', models.CharField(max_length=50)),
                ('trophy_year', models.DateField()),
                ('trophy_image', models.ImageField(default='trophy.png', upload_to='images/')),
            ],
            options={
                'verbose_name_plural': 'Trophy Manager',
            },
        ),
        migrations.AlterField(
            model_name='connect_message',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 12, 10, 51, 13, 989059, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='club_managers',
            name='manager_trophy',
            field=models.ManyToManyField(to='team.Trophy_manager'),
        ),
    ]
