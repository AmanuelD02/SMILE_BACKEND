# Generated by Django 3.2.8 on 2021-12-12 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankInfo',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('account_number', models.CharField(max_length=255)),
                ('ifsc', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CardInfo',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('card_num', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DepositTransaction',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Deposit', 'Deposit'), ('WithDrawal', 'WithDrawal')], max_length=100)),
                ('payment_id', models.CharField(max_length=255)),
                ('order_id', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='users.user')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_date', models.DurationField(auto_created=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('service_type', models.CharField(choices=[('Treatment', 'Treatment'), ('Consultation', 'Consultation'), ('Appointment', 'Appointment')], default='Appointment', max_length=100)),
                ('payer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_payer', to=settings.AUTH_USER_MODEL)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_reciever', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FundAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fund_account', models.CharField(max_length=255)),
                ('account_type', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_fund_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_id', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='fundaccount',
            constraint=models.UniqueConstraint(fields=('user_id', 'account_type'), name='FundAccount'),
        ),
    ]
