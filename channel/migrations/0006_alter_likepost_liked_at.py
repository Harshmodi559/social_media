# Generated by Django 4.0.4 on 2022-07-27 00:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_likepost_liked_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='liked_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
