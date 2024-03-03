# Generated by Django 5.0.2 on 2024-03-01 15:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money_amount', models.BigIntegerField(default=0, verbose_name='Сумма денег на счёте')),
                ('currency', models.CharField(choices=[('RUB', 'Рубль'), ('USD', 'Доллар')], default='RUB', verbose_name='Валюта хранения')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Владелец кошелька')),
            ],
            options={
                'verbose_name': 'Кошелёк',
                'verbose_name_plural': 'Кошельки',
                'ordering': ('user', 'currency'),
            },
        ),
    ]