# Generated by Django 3.1.5 on 2021-01-28 23:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('census_data', '0002_censustablepointer'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='censustablepointer',
            unique_together={('value_table', 'dataset')},
        ),
    ]
