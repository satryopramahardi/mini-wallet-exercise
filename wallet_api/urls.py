# from django.conf.urls import url
from django.urls import path, include
from .views import initialize_customer_api, wallet_api, deposit_api, withdrawal_api

urlpatterns = [
    path('init', initialize_customer_api),
    path('wallet', wallet_api),
    path('wallet/deposits', deposit_api),
    path('wallet/withdrawals', withdrawal_api)
]