from django.urls import path
from .views import NotificationView

url_patterns = [
    path('',NotificationView.as_view()),
]