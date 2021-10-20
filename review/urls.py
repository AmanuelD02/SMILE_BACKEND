from django.urls import path
from .views import ReviewLikeListView, ReviewLikeView, ReviewDetailView, ReviewView

urlpatterns = [
    path('', ReviewView.as_view()),
    path('<int:review_id>/like', ReviewLikeView.as_view()),
    path('<int:review_id>', ReviewDetailView.as_view()),
    path('likes/list',ReviewLikeListView.as_view()),
]