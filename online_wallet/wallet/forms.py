from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from wallet.choices import currencies
from wallet.models import WalletsHistory, Wallet

class TransferMoneyForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        from_wallet = kwargs.pop('from_wallet', None)
        super().__init__(*args, **kwargs)
        self.fields['to_wallet'].queryset = Wallet.objects.filter(~Q(id=from_wallet.id) & Q(currency=from_wallet.currency))
        self.fields['balance'].help_text = f'(Доступно {from_wallet.balance})'

    class Meta:
        model = WalletsHistory
        fields = ('to_wallet', 'balance',)

