from django.urls import path, include
from .views import RegisterView, SendOTPView, AuthenticateOTPView

urlpatterns = [
    path('authenticate/get_otp', SendOTPView.as_view()),
    path('authenticate/verify_code', AuthenticateOTPView.as_view()),
    path('register', RegisterView.as_view()),
]
