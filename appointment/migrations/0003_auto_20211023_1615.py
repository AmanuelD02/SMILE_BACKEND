# Generated by Django 3.2.8 on 2021-10-23 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0002_rename_avaiable_at_pendingappointment_available_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointment',
            old_name='avaiable_at',
            new_name='available_at',
        ),
        migrations.RenameField(
            model_name='availability',
            old_name='avaialble_at',
            new_name='available_at',
        ),
    ]