from django.urls import path
from .views import RegisterView, SendOTPView, AuthenticateOTPView
from .views import AddressDetailView, AddressView, DentistDetailView, DentistView,\
    LinkView, LocationView, LocationDetailView, LinkDetailView, EditProfileView, \
        DentistAllInfoView, SearchDentistListView


urlpatterns = [
    path('authenticate/get_otp', SendOTPView.as_view()),
    path('authenticate/verify_code', AuthenticateOTPView.as_view()),
    path('register', RegisterView.as_view()),
    path('edit_profile', EditProfileView.as_view()),

    path('location/<int:id>/', LocationDetailView.as_view()),
    path('location/', LocationView.as_view()),

    path('address/<int:id>/', AddressDetailView.as_view()),
    path('address/', AddressView.as_view()),

    path('link/<int:id>/', LinkDetailView.as_view()),
    path('link/', LinkView.as_view()),

    path('dentist/<int:id>/', DentistDetailView.as_view()),
    path('dentist/', DentistView.as_view()),
    path('dentist/all/<int:id>/',DentistAllInfoView.as_view()),
    path('dentist/search/',SearchDentistListView.as_view()),
]
