# Generated by Django 3.2 on 2021-04-08 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0018_auto_20210405_1744'),
    ]

    operations = [
        migrations.RenameField(
            model_name='value',
            old_name='region',
            new_name='geog',
        ),
    ]
