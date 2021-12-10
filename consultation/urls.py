from django.urls import path

from .views import PendingConsultationView, PendingConsultationDetailView, PendingConsultationListView, ApproveConsultationView

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:consultation_chat_id>/',
         views.consultation_chat, name='consultation_chat'),

    path('pending/', PendingConsultationView.as_view()),
    path('pending/list', PendingConsultationListView.as_view()),
    path('pending/<int:pending_id>', PendingConsultationDetailView.as_view()),
    path('approve/<int:pending_id>/', ApproveConsultationView.as_view()),
    # path('message/', ConsultationMessageView.as_view()),
    # path('message/list/', GetConsultationMessageView.as_view()),
]
