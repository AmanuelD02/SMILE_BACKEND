from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q, fields
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from .models import Consultation, ConsultationMessage, PendingConsultation
from .serializer import PendingConsultationSerializer, ConsultationMessageSerializer

# Create your views here.


def index(request):
    return render(request, 'consultation/index.html')


def consultation_chat(request, consultation_chat_id):
    return render(request, 'consultation/room.html', {
        'chat_name': consultation_chat_id
    })


def PendingConsultationView(APIView):
    def post(self, request):
        try:
            serializer = PendingConsultationSerializer(request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
            return Response(serializer.data)
        except ValueError as e:
            if e.message == "Low Balance":
                return Response({"message": "Low Balance"}, status=status.HTTP_400_BAD_REQUEST)
            elif e.message == "Dentist Not Available":
                return Response({"message": "Invalid Availability"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"message": "Unknown Error"}, status=status.HTTP_400_BAD_REQUEST)


class PendingConsultationDetailView(APIView):
    def get(self, request, pending_id):
        pending_consultation = get_object_or_404(
            PendingConsultation, pk=pending_id)
        serializer = PendingConsultationSerializer(pending_consultation)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pending_id):
        pending_consultation = get_object_or_404(
            PendingConsultation, pk=pending_id)
        pending_consultation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PendingConsultationListView(ListAPIView):
    serializer_class = PendingConsultationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        queryset = PendingConsultation.objects.filter(
            dentist_id=dentist_id).order_by('created_at')

        return queryset


class ApproveConsultationView(APIView):
    def post(self, request, pending_id):
        pending_consultation = get_object_or_404(
            PendingConsultation, pk=pending_id)

        try:
            with transaction.atomic():
                consultation = Consultation()
                consultation.dentist_id = pending_consultation.dentist_id
                consultation.user_id = pending_consultation.user_id
                consultation.status = 'o'

                pending_consultation.delete()
                serializer = ConsultationSerialier(consultation)

                return Response(serializer.data)
        except:
            return Response({"message": "Invalid Action"}, status=status.HTTP_400_BAD_REQUEST)
