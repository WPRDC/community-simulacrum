# Generated by Django 3.1.5 on 2021-01-28 15:54

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('geo', '0001_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataViz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Data Visualization',
                'verbose_name_plural': 'Data Visualizations',
            },
        ),
        migrations.CreateModel(
            name='Indicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('long_description', models.TextField(blank=True, help_text='A thorough description for long-form representation.', null=True)),
                ('limitations', models.TextField(blank=True, help_text='Describe what limitations the data may have (e.g. small sample size, difficulties in collecting data', null=True)),
                ('importance', models.TextField(blank=True, help_text='Describe the data collection process, highlighting areas where bias and assumptions made during the collection can impact how the data are interpreted', null=True)),
                ('source', models.TextField(blank=True, help_text='Describe the data collection process, highlighting areas where bias and assumptions made during the collection can impact how the data are interpreted', null=True)),
                ('provenance', models.TextField(blank=True, help_text='Describe the data collection process, highlighting areas where bias and assumptions made during the collection can impact how the data are interpreted', null=True)),
                ('layout', models.CharField(choices=[('A', 'Style A'), ('B', 'Style B'), ('C', 'Style C'), ('D', 'Style D')], default='A', max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MapLayer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('visible', models.BooleanField()),
                ('limit_to_target_geog', models.BooleanField(default=True)),
                ('custom_paint', models.JSONField(blank=True, help_text='https://docs.mapbox.com/help/glossary/layout-paint-property/', null=True)),
                ('custom_layout', models.JSONField(blank=True, help_text='https://docs.mapbox.com/help/glossary/layout-paint-property/', null=True)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_indicators.maplayer_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('time_coverage_start', models.DateTimeField()),
                ('time_coverage_end', models.DateTimeField(blank=True, help_text='Leave blank for indefinite', null=True)),
                ('time_granularity', models.IntegerField(choices=[(1, 'Minutely'), (2, 'Hourly'), (3, 'Daily'), (4, 'Weekly'), (5, 'Monthly'), (6, 'Quarterly'), (7, 'Yearly')], help_text='Select the smallest unit of time this source can aggregate to')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_indicators.source_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='TimeAxis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit', models.IntegerField(choices=[(1, 'Minutely'), (2, 'Hourly'), (3, 'Daily'), (4, 'Weekly'), (5, 'Monthly'), (6, 'Quarterly'), (7, 'Yearly')])),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_indicators.timeaxis_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='Variable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('units', models.CharField(blank=True, max_length=30, null=True)),
                ('unit_notes', models.CharField(blank=True, max_length=50, null=True)),
                ('percent_label_text', models.CharField(blank=True, help_text='Label to use when being used as denominator. If not provided, "% of &lt;title&gt;" will be used', max_length=100, null=True)),
                ('depth', models.IntegerField(default=0, help_text='Used to represent hierarchy of data. In practice, it is used to indent rows in a table corresponding to this variable')),
                ('denominators', models.ManyToManyField(blank=True, help_text='Variables that represent a universe under which the current variable can be analyzed', to='indicators.Variable')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_indicators.variable_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='BarChart',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('legendType', models.CharField(choices=[('line', 'Line'), ('square', 'Square'), ('rect', 'Rectangle'), ('circle', 'Circle'), ('cross', 'Cross'), ('diamond', 'Diamond'), ('star', 'Star'), ('triangle', 'Triangle'), ('wye', 'Wye'), ('none', 'None')], default='circle', max_length=10)),
                ('layout', models.CharField(choices=[('horizontal', 'Horizontal'), ('vertical', 'Vertical')], default='horizontal', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='BigValue',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('note', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='CensusSource',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.source')),
                ('dataset', models.CharField(choices=[('CEN', 'Decennial Census'), ('ACS5', 'ACS 5-year'), ('ACS1', 'ACS 1-year')], default='CEN', max_length=4)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.source',),
        ),
        migrations.CreateModel(
            name='CensusVariable',
            fields=[
                ('variable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.variable')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.variable',),
        ),
        migrations.CreateModel(
            name='ChoroplethLayer',
            fields=[
                ('maplayer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.maplayer')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.maplayer',),
        ),
        migrations.CreateModel(
            name='CKANSource',
            fields=[
                ('source_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.source')),
                ('package_id', models.UUIDField()),
                ('resource_id', models.UUIDField()),
                ('time_field', models.CharField(blank=True, help_text='Must be provided unless time coverage fits within 1 unit. i.e. this source only covers one unit of time (e.g. a 2042 dog census)', max_length=255, null=True)),
                ('time_field_format', models.CharField(blank=True, max_length=255, null=True)),
                ('standardization_query', models.TextField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.source', models.Model),
        ),
        migrations.CreateModel(
            name='LineChart',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('legendType', models.CharField(choices=[('line', 'Line'), ('square', 'Square'), ('rect', 'Rectangle'), ('circle', 'Circle'), ('cross', 'Cross'), ('diamond', 'Diamond'), ('star', 'Star'), ('triangle', 'Triangle'), ('wye', 'Wye'), ('none', 'None')], default='circle', max_length=10)),
                ('layout', models.CharField(choices=[('horizontal', 'Horizontal'), ('vertical', 'Vertical')], default='horizontal', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='ObjectsLayer',
            fields=[
                ('maplayer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.maplayer')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.maplayer',),
        ),
        migrations.CreateModel(
            name='ParcelsLayer',
            fields=[
                ('maplayer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.maplayer')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.maplayer',),
        ),
        migrations.CreateModel(
            name='PieChart',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('legendType', models.CharField(choices=[('line', 'Line'), ('square', 'Square'), ('rect', 'Rectangle'), ('circle', 'Circle'), ('cross', 'Cross'), ('diamond', 'Diamond'), ('star', 'Star'), ('triangle', 'Triangle'), ('wye', 'Wye'), ('none', 'None')], default='circle', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='PopulationPyramidChart',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('legendType', models.CharField(choices=[('line', 'Line'), ('square', 'Square'), ('rect', 'Rectangle'), ('circle', 'Circle'), ('cross', 'Cross'), ('diamond', 'Diamond'), ('star', 'Star'), ('triangle', 'Triangle'), ('wye', 'Wye'), ('none', 'None')], default='circle', max_length=10)),
            ],
            options={
                'abstract': False,
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='RelativeTimeAxis',
            fields=[
                ('timeaxis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.timeaxis')),
                ('start_offset', models.IntegerField(help_text='start time will be <this value> * <units> offset from the day its accessed; negative to go back in time (e.g. if unit is weeks, use -2 for axis to start 2 weeks prior to moment of viewing')),
                ('ticks', models.IntegerField(help_text='number of units')),
                ('direction', models.IntegerField(choices=[(-1, 'Backward'), (1, 'Forward')], default=-1)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.timeaxis',),
        ),
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('text', models.TextField(help_text='To place a value in your sentence, use {order}. e.g. "There are {1} cats and {2} dogs in town."')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='StaticConsecutiveTimeAxis',
            fields=[
                ('timeaxis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.timeaxis')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('ticks', models.IntegerField()),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.timeaxis',),
        ),
        migrations.CreateModel(
            name='StaticTimeAxis',
            fields=[
                ('timeaxis_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.timeaxis')),
                ('dates', django.contrib.postgres.fields.ArrayField(base_field=models.DateTimeField(), size=None)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.timeaxis',),
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('transpose', models.BooleanField(default=False)),
                ('show_percent', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.dataviz',),
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(blank=True, null=True)),
                ('margin', models.FloatField(blank=True, null=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geo.geography')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='indicators.variable')),
            ],
        ),
        migrations.CreateModel(
            name='Subdomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('indicators', models.ManyToManyField(blank=True, related_name='groups', to='indicators.Indicator')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='maplayer',
            name='variable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_map', to='indicators.variable'),
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('subdomains', models.ManyToManyField(blank=True, related_name='domains', to='indicators.Subdomain')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='dataviz',
            name='indicator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_vizes', to='indicators.indicator'),
        ),
        migrations.AddField(
            model_name='dataviz',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_indicators.dataviz_set+', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='dataviz',
            name='time_axis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data_vizes', to='indicators.timeaxis'),
        ),
        migrations.CreateModel(
            name='CKANGeomSource',
            fields=[
                ('ckansource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.ckansource')),
                ('geom_field', models.CharField(blank=True, default='_geom', max_length=100, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.ckansource',),
        ),
        migrations.CreateModel(
            name='CKANRegionalSource',
            fields=[
                ('ckansource_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.ckansource')),
                ('blockgroup_field', models.CharField(blank=True, max_length=100, null=True)),
                ('blockgroup_field_is_sql', models.BooleanField(default=False)),
                ('tract_field', models.CharField(blank=True, max_length=100, null=True)),
                ('tract_field_is_sql', models.BooleanField(default=False)),
                ('countysubdivision_field', models.CharField(blank=True, max_length=100, null=True)),
                ('countysubdivision_field_is_sql', models.BooleanField(default=False)),
                ('place_field', models.CharField(blank=True, max_length=100, null=True)),
                ('place_field_is_sql', models.BooleanField(default=False)),
                ('neighborhood_field', models.CharField(blank=True, max_length=100, null=True)),
                ('neighborhood_field_is_sql', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.ckansource',),
        ),
        migrations.CreateModel(
            name='TableRow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_table', to='indicators.variable')),
                ('table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='table_to_variable', to='indicators.table')),
            ],
            options={
                'unique_together': {('table', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='table',
            name='vars',
            field=models.ManyToManyField(through='indicators.TableRow', to='indicators.Variable', verbose_name='Rows'),
        ),
        migrations.CreateModel(
            name='SentenceVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_sentence', to='indicators.variable')),
                ('alphanumeric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sentence_to_variable', to='indicators.sentence')),
            ],
            options={
                'unique_together': {('alphanumeric', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='sentence',
            name='vars',
            field=models.ManyToManyField(through='indicators.SentenceVariable', to='indicators.Variable'),
        ),
        migrations.CreateModel(
            name='PopulationPyramidChartPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_population_pyramid_chart', to='indicators.variable')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='population_pyramid_chart_to_variable', to='indicators.populationpyramidchart')),
            ],
            options={
                'unique_together': {('chart', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='populationpyramidchart',
            name='vars',
            field=models.ManyToManyField(through='indicators.PopulationPyramidChartPart', to='indicators.Variable'),
        ),
        migrations.CreateModel(
            name='PieChartPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_pie_chart', to='indicators.variable')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pie_chart_to_variable', to='indicators.piechart')),
            ],
            options={
                'unique_together': {('chart', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='piechart',
            name='vars',
            field=models.ManyToManyField(through='indicators.PieChartPart', to='indicators.Variable'),
        ),
        migrations.CreateModel(
            name='MiniMap',
            fields=[
                ('dataviz_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.dataviz')),
                ('vars', models.ManyToManyField(through='indicators.MapLayer', to='indicators.Variable', verbose_name='Layers')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.dataviz',),
        ),
        migrations.AddField(
            model_name='maplayer',
            name='map',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='map_to_variable', to='indicators.minimap'),
        ),
        migrations.CreateModel(
            name='LineChartPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_line_chart', to='indicators.variable')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='line_chart_to_variable', to='indicators.linechart')),
            ],
            options={
                'unique_together': {('chart', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='linechart',
            name='vars',
            field=models.ManyToManyField(through='indicators.LineChartPart', to='indicators.Variable'),
        ),
        migrations.CreateModel(
            name='CKANVariable',
            fields=[
                ('variable_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='indicators.variable')),
                ('aggregation_method', models.CharField(choices=[('NONE', 'None'), ('COUNT', 'Count'), ('SUM', 'Sum'), ('AVG', 'Mean'), ('MODE', 'Mode'), ('MAX', 'Maximum'), ('MIN', 'Minimum')], default='COUNT', max_length=5)),
                ('field', models.CharField(help_text='field in source to aggregate', max_length=100)),
                ('sql_filter', models.TextField(blank=True, help_text='SQL clause that will be used to filter data.', null=True)),
                ('carto_table', models.CharField(blank=True, max_length=60, null=True, verbose_name='Carto Table')),
                ('field_in_carto', models.CharField(blank=True, help_text='If left blank, the value for "field" will be used.', max_length=60, null=True, verbose_name='Carto field')),
                ('sql_filter_for_carto', models.TextField(blank=True, help_text='If left blank, the value for "sql filter" will be used.', null=True, verbose_name='Carto SQL Filter')),
                ('sources', models.ManyToManyField(related_name='ckan_variables', to='indicators.CKANSource')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('indicators.variable',),
        ),
        migrations.CreateModel(
            name='CensusVariableSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formula', models.TextField()),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_to_variable', to='indicators.censussource')),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_source', to='indicators.censusvariable')),
            ],
        ),
        migrations.AddField(
            model_name='censusvariable',
            name='sources',
            field=models.ManyToManyField(related_name='census_variables', through='indicators.CensusVariableSource', to='indicators.CensusSource'),
        ),
        migrations.CreateModel(
            name='BigValueVariable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_big_value', to='indicators.variable')),
                ('alphanumeric', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='big_value_to_variable', to='indicators.bigvalue')),
            ],
            options={
                'unique_together': {('alphanumeric', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='bigvalue',
            name='vars',
            field=models.ManyToManyField(through='indicators.BigValueVariable', to='indicators.Variable'),
        ),
        migrations.CreateModel(
            name='BarChartPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField()),
                ('variable', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variable_to_bar_chart', to='indicators.variable')),
                ('chart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bar_chart_to_variable', to='indicators.barchart')),
            ],
            options={
                'unique_together': {('chart', 'variable', 'order')},
            },
        ),
        migrations.AddField(
            model_name='barchart',
            name='vars',
            field=models.ManyToManyField(through='indicators.BarChartPart', to='indicators.Variable'),
        ),
    ]
