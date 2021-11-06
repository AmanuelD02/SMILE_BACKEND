from django.urls import path
from .views import WalletView

url_patterns = [
    path('wallet/', WalletView.as_view()),
]
