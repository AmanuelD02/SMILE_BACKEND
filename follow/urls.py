from django.urls import path, include
from .views import FollowView, FollowDetailView



urlpatterns = [
        path('',FollowView.as_view()),
        path('<int:dentist_id>/', FollowDetailView.as_view())

]