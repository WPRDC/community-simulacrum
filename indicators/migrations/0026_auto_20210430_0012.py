# Generated by Django 3.2 on 2021-04-30 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0025_alter_bigvalue_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chart',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('legendType', models.CharField(choices=[('line', 'Line'), ('square', 'Square'), ('rect', 'Rectangle'), ('circle', 'Circle'), ('cross', 'Cross'), ('diamond', 'Diamond'), ('star', 'Star'), ('triangle', 'Triangle'), ('wye', 'Wye'), ('none', 'None')], default='circle', max_length=10)),
                ('across_geogs', models.BooleanField(default=False, help_text='Check if you want this chart to compare the statistic across geographies instead of across time')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='ChartPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='barchartpart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='barchartpart',
            name='variable',
        ),
        migrations.RemoveField(
            model_name='barchartpart',
            name='viz',
        ),
        migrations.RemoveField(
            model_name='linechart',
            name='dataviz_ptr',
        ),
        migrations.RemoveField(
            model_name='linechart',
            name='vars',
        ),
        migrations.AlterUniqueTogether(
            name='linechartpart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='linechartpart',
            name='variable',
        ),
        migrations.RemoveField(
            model_name='linechartpart',
            name='viz',
        ),
        migrations.RemoveField(
            model_name='piechart',
            name='dataviz_ptr',
        ),
        migrations.RemoveField(
            model_name='piechart',
            name='vars',
        ),
        migrations.AlterUniqueTogether(
            name='piechartpart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='piechartpart',
            name='variable',
        ),
        migrations.RemoveField(
            model_name='piechartpart',
            name='viz',
        ),
        migrations.RemoveField(
            model_name='populationpyramidchart',
            name='dataviz_ptr',
        ),
        migrations.RemoveField(
            model_name='populationpyramidchart',
            name='vars',
        ),
        migrations.AlterUniqueTogether(
            name='populationpyramidchartpart',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='populationpyramidchartpart',
            name='variable',
        ),
        migrations.RemoveField(
            model_name='populationpyramidchartpart',
            name='viz',
        ),
        migrations.RemoveField(
            model_name='ckanvariable',
            name='aggregation_method',
        ),
        migrations.RemoveField(
            model_name='dataviz',
            name='height_override',
        ),
        migrations.RemoveField(
            model_name='dataviz',
            name='width_override',
        ),
        migrations.AddField(
            model_name='variable',
            name='aggregation_method',
            field=models.CharField(choices=[('NONE', 'None'), ('COUNT', 'Count'), ('SUM', 'Sum'), ('AVG', 'Mean'), ('MODE', 'Mode'), ('MAX', 'Maximum'), ('MIN', 'Minimum')], default='SUM', max_length=5),
        ),
        migrations.DeleteModel(
            name='BarChart',
        ),
        migrations.DeleteModel(
            name='BarChartPart',
        ),
        migrations.DeleteModel(
            name='LineChart',
        ),
        migrations.DeleteModel(
            name='LineChartPart',
        ),
        migrations.DeleteModel(
            name='PieChart',
        ),
        migrations.DeleteModel(
            name='PieChartPart',
        ),
        migrations.DeleteModel(
            name='PopulationPyramidChart',
        ),
        migrations.DeleteModel(
            name='PopulationPyramidChartPart',
        ),
        migrations.AddField(
            model_name='chartpart',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_chart', to='indicators.variable'),
        ),
        migrations.AddField(
            model_name='chartpart',
            name='viz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chart_to_variable', to='indicators.chart'),
        ),
        migrations.AddField(
            model_name='chart',
            name='vars',
            field=models.ManyToManyField(through='indicators.ChartPart', to='indicators.Variable', verbose_name='Rows'),
        ),
        migrations.AlterUniqueTogether(
            name='chartpart',
            unique_together={('viz', 'variable', 'order')},
        ),
    ]
