from django.urls import path
from api.views import WalletListApiView, WalletDetailApiView, UserWalletsListApiView
urlpatterns = [
    path('users/<int:pk>/', UserWalletsListApiView.as_view()),
    path('wallets/', WalletListApiView.as_view()),
    path('wallets/<int:pk>/', WalletDetailApiView.as_view()),
]

