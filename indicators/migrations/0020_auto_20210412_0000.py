# Generated by Django 3.2 on 2021-04-12 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0019_rename_region_value_geog'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sentencevariable',
            options={'ordering': ['order']},
        ),
        migrations.RenameField(
            model_name='barchartpart',
            old_name='chart',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='bigvaluevariable',
            old_name='alphanumeric',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='linechartpart',
            old_name='chart',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='maplayer',
            old_name='minimap',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='piechartpart',
            old_name='chart',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='populationpyramidchartpart',
            old_name='chart',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='sentencevariable',
            old_name='alphanumeric',
            new_name='viz',
        ),
        migrations.RenameField(
            model_name='tablerow',
            old_name='table',
            new_name='viz',
        ),
        migrations.AddField(
            model_name='linechartpart',
            name='style',
            field=models.CharField(blank=True, choices=[(None, 'None'), ('HI', 'Highlight'), ('SU', 'Subtle'), ('AVG', 'Avg/Mean')], default=None, max_length=4, null=True, verbose_name='Special Style'),
        ),
        migrations.AddField(
            model_name='piechartpart',
            name='style',
            field=models.CharField(blank=True, choices=[(None, 'None'), ('HI', 'Highlight'), ('SU', 'Subtle'), ('AVG', 'Avg/Mean')], default=None, max_length=4, null=True, verbose_name='Special Style'),
        ),
        migrations.AddField(
            model_name='populationpyramidchartpart',
            name='style',
            field=models.CharField(blank=True, choices=[(None, 'None'), ('HI', 'Highlight'), ('SU', 'Subtle'), ('AVG', 'Avg/Mean')], default=None, max_length=4, null=True, verbose_name='Special Style'),
        ),
        migrations.AlterUniqueTogether(
            name='barchartpart',
            unique_together={('viz', 'variable', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='bigvaluevariable',
            unique_together={('viz', 'variable', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='linechartpart',
            unique_together={('viz', 'variable', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='piechartpart',
            unique_together={('viz', 'variable', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='populationpyramidchartpart',
            unique_together={('viz', 'variable', 'order')},
        ),
        migrations.AlterUniqueTogether(
            name='sentencevariable',
            unique_together=set(),
        ),
        migrations.AlterUniqueTogether(
            name='tablerow',
            unique_together={('viz', 'variable', 'order')},
        ),
    ]
