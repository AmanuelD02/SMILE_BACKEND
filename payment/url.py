from django.urls import path
from .views import WalletView, UpdateContact, PerformPayment

url_patterns = [
    path('wallet/', WalletView.as_view()),
    path('update_contact/', UpdateContact.as_view()),
    path('payment/', PerformPayment.as_view())
]
