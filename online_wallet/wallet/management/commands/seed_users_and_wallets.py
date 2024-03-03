import logging
import os
import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from faker import factory, Faker
from wallet.models import Wallet
from wallet.choices import currencies

fake = Faker(['ru-RU'])

class Command(BaseCommand):
    help_message = "seeding database with users and theirs wallets"
    result_message = 'done'
    test_password = 'test'
    users_count = 10
    min_balance = 0
    max_balance = 250000
    chance_to_have_two_wallets = 25 # 25 of 100 %

    def create_user(self, password):
        return User.objects.create(
            username=fake.user_name(),
            email=fake.email(),
            password=make_password('test'),
            is_staff=True,
            is_active=True,
            is_superuser=True,
        )

    def create_wallet(self, user):
        return Wallet.objects.create(
            owner=user,
            balance=random.randint(self.min_balance, self.max_balance),
            currency=random.choice(currencies)[0],
        )

    def handle(self, *args, **options):
        self.stdout.write(self.help_message)
        for _ in range(self.users_count):
            user = self.create_user(self.test_password)
            wallet = self.create_wallet(user)
            if random.randint(0, 100) == self.chance_to_have_two_wallets:
                self.create_wallet(user)
            user.save()


        self.stdout.write(self.result_message)
