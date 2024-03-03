from django.contrib import admin
from django.urls import path, include
from wallet import urls as wallet_urls
from api import urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include((wallet_urls, 'wallet'), namespace='wallets')),
    path('api/', include(api_urls))
]

