# Generated by Django 5.1.4 on 2024-12-15 18:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='duracion',
            field=models.DurationField(default=datetime.timedelta(seconds=7200)),
        ),
    ]
