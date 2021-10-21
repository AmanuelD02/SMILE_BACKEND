# Generated by Django 3.2.8 on 2021-10-21 02:06

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20211020_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_pic_path',
            field=models.ImageField(default='media\\default.png', upload_to=users.models.upload_to),
        ),
    ]
