from django.urls import path
from .views import WalletView, UpdateContact, PerformPayment

urlpatterns = [
    path('wallet/', WalletView.as_view()),
    path('update_contact/', UpdateContact.as_view()),
    path('', PerformPayment.as_view())
]
