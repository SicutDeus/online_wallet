from django.contrib.auth.models import User
from rest_framework import generics
from wallet.models import Wallet
from api.serializers import WalletSerializer, WalletDetailSerializer
from rest_framework import generics
from rest_framework import mixins

class UserWalletsListApiView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(owner__id=kwargs.get('pk'))
        return super().list(request, *args, **kwargs)


class WalletListApiView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class WalletDetailApiView(mixins.RetrieveModelMixin,
                    generics.GenericAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)



