# Generated by Django 3.2.8 on 2021-11-15 10:41

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0003_auto_20211114_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clinic',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, srid=4326),
        ),
    ]
