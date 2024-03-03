from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin as prev_UserAdmin
from .models import Wallet, WalletsHistory
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User


class WalletInlineForm(forms.ModelForm):

    class Meta:
        fields = ('__all__')
        model = Wallet


class WalletAdmin(InlineModelAdmin):
    model = Wallet

class WalletInline(admin.StackedInline):
    model = Wallet
    extra = 0

class UserAdmin(prev_UserAdmin):
    inlines = [WalletInline, ]


admin.site.register(Wallet)
admin.site.register(WalletsHistory)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)



