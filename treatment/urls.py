from django.urls import path
from .views import   TreatmentDetailView, TreatmentListView, TreatmentNameListView, TreatmentNameDetailView, TreatmentView, TreatmentNameView,TreatmentView

urlpatterns = [
    path('',TreatmentView.as_view()),
    path('name/list/', TreatmentNameListView.as_view()),
    path('name/', TreatmentNameView.as_view()),
    path('name/<int:treatment_name_id>/', TreatmentNameDetailView.as_view()),
    path('<int:treatment_id>/',TreatmentDetailView.as_view()),
    path('list/', TreatmentListView.as_view()),


 ]