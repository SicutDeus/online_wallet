from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from wallet.choices import currencies


class Wallet(models.Model):
    owner = models.ForeignKey(to=User, verbose_name='Владелец кошелька', on_delete=models.CASCADE)
    balance = models.BigIntegerField(verbose_name='Сумма денег на счёте', default=0)
    currency = models.CharField('Валюта хранения', choices=currencies, default='RUB')

    def __str__(self):
        return f'Кошелёк {self.owner} ({self.currency})'

    def get_absolute_url(self):
        return reverse("wallets:wallet_detail", args=[self.owner.id, self.id])

    class Meta:
        verbose_name = 'Кошелёк'
        verbose_name_plural = 'Кошельки'
        ordering = ('owner', 'currency')


class WalletsHistory(models.Model):
    from_wallet = models.ForeignKey(Wallet, verbose_name='Кошелёк, откуда переводить', on_delete=models.SET_NULL, null=True, related_name='from_wallet')
    to_wallet = models.ForeignKey(Wallet, verbose_name='Кошелёк, куда переводить', on_delete=models.SET_NULL, null=True, related_name='to_wallet')
    balance = models.BigIntegerField(verbose_name='Сумма денег для перевода', default=0)
    currency = models.CharField('Валюта хранения', choices=currencies, default='RUB')
    created_at = models.DateTimeField(verbose_name='Дата перевода', auto_created=True, auto_now_add=True)

    class Meta:
        verbose_name = 'История перевода'
        verbose_name_plural = 'Истории переводов'
        ordering = ('-created_at',)

    def get_absolute_url(self):
        return reverse("wallets:wallet_detail", args=[self.from_wallet.owner.id, self.from_wallet.id])

    def __str__(self):
        return f'История перевода {self.from_wallet} -> {self.to_wallet}'


