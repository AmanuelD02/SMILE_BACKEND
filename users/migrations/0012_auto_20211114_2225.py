# Generated by Django 3.2.8 on 2021-11-14 19:25

import django.contrib.gis.db.models.fields
from django.db import migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_dentist_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='location',
            name='longtiude',
        ),
        migrations.AddField(
            model_name='location',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(default=django.utils.timezone.now, srid=4326),
            preserve_default=False,
        ),
    ]