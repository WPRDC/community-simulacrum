# Generated by Django 3.1.5 on 2021-03-17 23:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('indicators', '0015_auto_20210309_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='subdomains',
        ),
        migrations.AddField(
            model_name='subdomain',
            name='domain',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='subdomains', to='indicators.domain'),
            preserve_default=False,
        ),
    ]
