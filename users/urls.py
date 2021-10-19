from django.urls import path, include
from .views import  AddressDetailView, AddressView, DentistDetailView, DentistView,\
                     LinkView, LocationView, LocationDetailView, LinkDetailView

urlpatterns = [
    
    
    path('location/<int:id>/', LocationDetailView.as_view()),
    path('location/', LocationView.as_view()),

    path('address/<int:id>/', AddressDetailView.as_view()),
    path('address/', AddressView.as_view()),

    path('link/<int:id>/', LinkDetailView.as_view()),
    path('link/',LinkView.as_view()),

    path('dentist/<int:id>/', DentistDetailView.as_view()),
    path('dentist/',DentistView.as_view()),
]
