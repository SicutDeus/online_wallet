from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers

from wallet.models import Wallet, WalletsHistory

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'owner', 'balance', 'currency')


class WalletHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletsHistory
        fields = ('from_wallet', 'to_wallet', 'balance', 'currency')

class WalletDetailSerializer(WalletSerializer):
    changes = serializers.SerializerMethodField()

    def get_changes(self, obj):
        return WalletHistorySerializer(WalletsHistory.objects.filter(Q(from_wallet=obj) | Q(to_wallet=obj)), many=True).data

    class Meta:
        model = Wallet
        fields = ('id', 'owner', 'balance', 'currency', 'changes')

