# Generated by Django 4.0.4 on 2022-08-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0004_remove_post_str_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='str_id',
            field=models.CharField(max_length=500, null=True),
        ),
    ]