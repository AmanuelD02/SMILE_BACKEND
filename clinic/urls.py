from django.urls import path
from .views import ClinicView, ClinicSearchView, ClinicDetailView

urlpatterns = [
    path('',ClinicView.as_view()),
    path('<int:clinic_id>/', ClinicDetailView.as_view()),
    path('list/',ClinicSearchView.as_view()),
]