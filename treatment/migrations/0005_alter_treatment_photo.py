# Generated by Django 3.2.8 on 2021-10-22 22:32

from django.db import migrations, models
import treatment.models


class Migration(migrations.Migration):

    dependencies = [
        ('treatment', '0004_alter_treatment_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='photo',
            field=models.ImageField(
                default='medical\\medical_service.png', upload_to=treatment.models.upload_to),
        ),
    ]
