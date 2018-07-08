# Generated by Django 2.0.2 on 2018-06-21 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180621_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='feed',
            name='url',
            field=models.URLField(unique=True),
        ),
    ]