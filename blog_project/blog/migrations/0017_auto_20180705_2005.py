# Generated by Django 2.0.2 on 2018-07-06 01:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20180705_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 5, 20, 5, 4, 450289, tzinfo=utc)),
        ),
    ]