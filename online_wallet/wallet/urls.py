from django.urls import path, include
from django.contrib.auth import views as auth_views
from wallet import views

urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('login/', auth_views.LoginView.as_view(template_name='wallets/login.html', success_url='wallets:user_list'), name='user_login'),
    path('<int:user_id>/wallets/', views.UserWalletsListView.as_view(), name='wallets_list'),
    path('<int:user_id>/wallets/create/', views.WalletCreateView.as_view(), name='wallet_create'),
    path('<int:user_id>/wallets/<int:pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),
    path('<int:user_id>/wallets/<int:pk>/transfer/', views.CreateTransferView.as_view(), name='wallet_transfer'),
]