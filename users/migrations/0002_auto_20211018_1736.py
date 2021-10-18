# Generated by Django 3.2.8 on 2021-10-18 14:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dentist',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('clinic_name', models.CharField(blank=True, max_length=255)),
                ('degree', models.CharField(blank=True, max_length=255)),
                ('appointment_rate', models.FloatField()),
                ('consultation_rate', models.FloatField()),
                ('experience_year', models.PositiveIntegerField()),
                ('document_path', models.CharField(max_length=255)),
                ('verified', models.BooleanField(default=False)),
                ('rating', models.PositiveSmallIntegerField()),
                ('consultation_availabilty', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('phone_num', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('code', models.IntegerField()),
                ('expiration_date', models.DateTimeField()),
            ],
        ),
        migrations.RenameField(
            model_name='user',
            old_name='password',
            new_name='profile_pic_path',
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.dentist')),
                ('country', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('state', models.CharField(blank=True, max_length=255)),
                ('street', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.dentist')),
                ('facebook', models.CharField(blank=True, max_length=255)),
                ('twitter', models.CharField(blank=True, max_length=255)),
                ('linkedin', models.CharField(blank=True, max_length=255)),
                ('whatsapp', models.CharField(blank=True, max_length=255)),
                ('telegram', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.dentist')),
                ('latitude', models.CharField(max_length=255)),
                ('longtiude', models.CharField(max_length=255)),
            ],
        ),
    ]
