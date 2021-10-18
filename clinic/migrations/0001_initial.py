# Generated by Django 3.2.8 on 2021-10-18 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('profilePic', models.CharField(blank=True, max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('latitude', models.CharField(blank=True, max_length=255)),
                ('longtitude', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
