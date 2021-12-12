from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.db.models import Q, fields
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from users.models import Dentist, User
from .models import Consultation, ConsultationMessage, PendingConsultation
from .serializer import ConsultationSerializer, PendingConsultationSerializer, ConsultationMessageSerializer

# Create your views here.


def index(request):
    return render(request, 'consultation/index.html')


def consultation_chat(request, consultation_chat_id):
    return render(request, 'consultation/room.html', {
        'chat_name': consultation_chat_id
    })


class PendingConsultationView(APIView):
    def post(self, request):
        try:
            serializer = PendingConsultationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            print("serializer is valid")
            serializer.save()
            print("serializer saved")
            return Response(serializer.data)
        except ValueError as e:
            if e.msg == "Low Balance":
                return Response({"message": "Low Balance"}, status=status.HTTP_400_BAD_REQUEST)
            elif e.msg == "Dentist Not Available":
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
                print("pending_is",pending_id)
                consultation = Consultation()
                print(pending_consultation.dentist_id,pending_consultation.user_id)
                # dentist = Dentist.objects.filter(id= pending_consultation.dentist_id).first()
                # print(dentist.id.id)
                print("dentist",pending_consultation.dentist_id.id.id)
                dentist = Dentist.objects.filter(id=pending_consultation.dentist_id.id.id).first()
                consultation.dentist_id =dentist
                print("user..")
                user = User.objects.filter(id=pending_consultation.user_id.id).first()
                consultation.user_id = user
                print("UU")
                consultation.status = 'o'
                consultation.duration = pending_consultation.duration

                serializer = ConsultationSerializer(consultation)
                print("ere plzz sera")
                consultation.save()
                print("saved?")
                pending_consultation.delete()

                return Response(serializer.data)
        except Exception as e:
            print("excption ",e)
            return Response({"message": "Invalid Exception"}, status=status.HTTP_400_BAD_REQUEST)
