# Generated by Django 3.1.5 on 2021-01-28 23:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('census_data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CensusTablePointer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataset', models.CharField(choices=[('CEN', 'Decennial Census'), ('ACS5', 'ACS 5-year'), ('ACS1', 'ACS 1-year')], default='CEN', max_length=4)),
                ('moe_table', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moe_to_pointer', to='census_data.censustable')),
                ('value_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='value_to_pointer', to='census_data.censustable')),
            ],
        ),
    ]
