# Generated by Django 3.2.8 on 2021-11-26 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('created_at', models.DateTimeField(auto_created=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('payment', 'payment'), ('review', 'review'), ('update_profile', 'update_profile'), ('appointment', 'appointment')], max_length=100)),
                ('content', models.TextField()),
                ('is_seen', models.BooleanField(default=False)),
            ],
        ),
    ]
