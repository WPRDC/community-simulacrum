# Generated by Django 3.1.5 on 2021-02-04 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('census_data', '0003_auto_20210128_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='censustablepointer',
            name='table_id',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]