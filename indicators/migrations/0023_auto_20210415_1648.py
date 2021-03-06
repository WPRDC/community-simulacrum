# Generated by Django 3.2 on 2021-04-15 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0022_auto_20210415_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maplayer',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_minimap', to='indicators.variable'),
        ),
        migrations.AlterField(
            model_name='maplayer',
            name='viz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='minimap_to_variable', to='indicators.minimap'),
        ),
    ]
