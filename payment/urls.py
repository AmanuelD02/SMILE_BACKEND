from django.urls import path

from payment.serializers import FundAccountSerializer
from .views import WalletView, UpdateContact, PerformPayment, BankInfoView, BankInfoDetailView, FundAccountView

urlpatterns = [
    path('wallet/', WalletView.as_view()),
    path('update_contact/', UpdateContact.as_view()),
    path('', PerformPayment.as_view()),
    path('bank_account/',BankInfoView.as_view()),
    path('bank_account/<int:id>/',BankInfoDetailView.as_view()),
    path('funds/<int:id>/',FundAccountView.as_view()),
]
