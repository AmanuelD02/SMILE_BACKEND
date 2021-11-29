# Generated by Django 3.2.8 on 2021-11-26 11:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('follow', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='follow',
            name='dentist_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.dentist'),
        ),
        migrations.AddField(
            model_name='follow',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user_id', 'dentist_id'), name='Follow'),
        ),
    ]
