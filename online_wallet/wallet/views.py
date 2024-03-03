import logging

import rest_framework.exceptions
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from django.db.models import Q
from django import forms
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.models import User
from wallet.models import Wallet, WalletsHistory
from wallet.forms import TransferMoneyForm


class UserWalletsListView(ListView):
    template_name = "wallets/wallet_list.html"
    model = Wallet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, id=self.kwargs.get('user_id'))
        context["wallets"] = Wallet.objects.filter(owner=user)
        context["owner"] = user
        return context


class WalletDetailView(DetailView):
    template_name = "wallets/wallet_card.html"
    model = Wallet
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        wallet = get_object_or_404(Wallet, id=self.kwargs.get('pk'))
        context["operations"] = WalletsHistory.objects.filter(
            Q(from_wallet=wallet) |
            Q(to_wallet=wallet)
        )
        context['wallet'] = wallet
        return context


class WalletCreateView(CreateView):
    template_name = "wallets/wallet_create.html"
    fields = ('currency', 'balance')
    model = Wallet

    def form_valid(self, form):
        user_id = self.kwargs.get('user_id')
        form.instance.owner = get_object_or_404(User, id=user_id)
        super().form_valid(form)
        with open('logs.txt', 'a+') as f:
            f.write(f'Created wallet for {form.instance.owner} in {form.instance.balance} {form.instance.currency}\n')
        return redirect('wallets:wallets_list', user_id)


class UserListView(ListView):
    template_name = "wallets/user_list.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

class CreateTransferView(CreateView):
    form_class = TransferMoneyForm
    template_name = 'wallets/money_transfer.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['from_wallet'] = get_object_or_404(Wallet, id=self.kwargs.get('pk'))
        return kwargs


    def form_valid(self, form):
        from_wallet = get_object_or_404(Wallet, id=self.kwargs.get('pk'))
        transfer_balance = form.cleaned_data['balance']
        to_wallet = form.cleaned_data['to_wallet']
        if from_wallet.balance < transfer_balance:
            form.add_error('balance', 'В кошельке не хватает средств')
            return self.form_invalid(form)
        form.instance.from_wallet = from_wallet
        form.instance.currency = from_wallet.currency
        with open('logs.txt', 'a+') as f:
            f.write(f'Added transfer from {from_wallet} to {form.instance.to_wallet} in {form.instance.balance} {form.instance.currency}\n')
        super().form_valid(form)

        from_wallet.balance -= transfer_balance
        from_wallet.save()
        to_wallet.balance += transfer_balance
        to_wallet.save()

        return redirect('wallets:wallets_list', self.kwargs.get('user_id'))
