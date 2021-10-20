from django.urls import path, include
from .views import FollowView, FollowDetailView,FollowDetailListView



urlpatterns = [
        path('',FollowView.as_view()),
        path('<int:dentist_id>/', FollowDetailView.as_view()),
        path('list',FollowDetailListView.as_view())

]