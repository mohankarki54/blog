# Generated by Django 2.0.2 on 2018-06-28 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20180625_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-publication_date']},
        ),
    ]