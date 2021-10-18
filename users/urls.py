from django.urls import path, include
from .views import  AddressDetailView, AddressView, DentistDetailView, DentistView,\
                     LinkView, LocationView, LocationDetailView, LinkDetailView

urlpatterns = [
    
    
    path('location/', LocationView.as_view()),
    path('location/detail/<int:id>/', LocationDetailView.as_view()),

    path('address/', AddressView.as_view()),
    path('address/detail/<int:id>/', AddressDetailView.as_view()),

    path('link/',LinkView.as_view()),
    path('link/detail/<int:id>/', LinkDetailView.as_view()),

    path('dentist/',DentistView.as_view()),
    path('dentist/detail/<int:id>/', DentistDetailView.as_view()),
]
