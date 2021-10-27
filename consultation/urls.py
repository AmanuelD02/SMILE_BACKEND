from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:consultation_chat_id>/',
         views.consultation_chat, name='consultation_chat')
]
