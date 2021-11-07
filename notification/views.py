from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer
# Create your views here.


class NotificationView(ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        reciever_id = self.request.query_params.get('reciever_id')
        queryset = Notification.objects.filter(reciever_id=reciever_id)
        return queryset.reverse()
