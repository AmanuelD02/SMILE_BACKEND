
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from datetime import datetime
from django.db.models import fields
from django.shortcuts import get_object_or_404
from django.db import models, transaction

from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from users.models import Dentist, User

from .models import Appointment, Availability, PendingAppointment
from .serializer import AppointmentMessageSerializer, AppointmentSerializer, AvailabiltySerializer, PendingAppointmentSerializer, PatientsSerializer
from appointment import serializer


# Create your views here.
class AvailabilityView(APIView):
    def post(self, request):
        serializer = AvailabiltySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class AvailabilityDetailView(APIView):
    def get(self, request, availabilty_id):
        available = get_object_or_404(Availability, pk=availabilty_id)
        serializer = AvailabiltySerializer(available)

        return Response(serializer.data)

    def delete(self, request, availabilty_id):
        available = get_object_or_404(Availability, pk=availabilty_id)
        available.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AvailabiltyListView(ListAPIView):
    serializer_class = AvailabiltySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        queryset = Availability.objects.filter(dentist_id=dentist_id)
        return queryset


class PendingAppointmentView(APIView):
    def post(self, request):
        serializer = PendingAppointmentSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        available = Availability.objects.filter(
            available_at=serializer.validated_data['available_at']).first()
        if available:
            serializer.save()
            return Response(serializer.data)

        return Response({"message": "Invalid Availability"}, status=status.HTTP_400_BAD_REQUEST)


class PendingAppointmentDetailView(APIView):
    def get(self, request, pending_id):
        pending = get_object_or_404(PendingAppointment, pk=pending_id)
        serializer = PendingAppointmentSerializer(pending)
        return Response(serializer.data)

    def delete(self, request, pending_id):
        pending = get_object_or_404(PendingAppointment, pk=pending_id)
        pending.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class PendingAppointmentListView(ListAPIView):
    serializer_class = PendingAppointmentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        queryset = PendingAppointment.objects.filter(
            dentist_id=dentist_id).order_by('available_at')
        return queryset


class AppointmentView(APIView):
    def post(self, request, pending_id):
        pending = get_object_or_404(PendingAppointment, pk=pending_id)

        available = Availability.objects.filter(
            available_at=pending.available_at).first()
        if available:
            with transaction.atomic():
                appointment = Appointment()
                appointment.available_at = pending.available_at
                appointment.dentist_id = pending.dentist_id
                appointment.user_id = pending.user_id
                appointment.treatment_id = pending.treatment_id

                available.delete()
                pending.delete()
                appointment.save()
                serializer = AppointmentSerializer(appointment)

                return Response(serializer.data)
            return Response({"message": "some error occured"}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"message": "not available"}, status=status.HTTP_400_BAD_REQUEST)


class AppointmentListView(ListAPIView):
    serializer_class = AppointmentView
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        user_id = self.request.query_params.get('user_id', None)
        queryset = Appointment.objects.filter(
            dentist_id=dentist_id, user_id=user_id)
        return queryset


class AppointmentDetailView(APIView):
    def get(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk=appointment_id)
        appointment.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AppointmentMessageView(APIView):
    def post(self, request):
        serializer = AppointmentMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class GetAppointmentMessageView(ListAPIView):
    serializer_class = AppointmentMessageSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('chat_id', None)
        queryset = PendingAppointment.objects.filter(dentist_id=dentist_id)
        return queryset.reverse()


# class GetAllPatientsView(APIView):
#     def get(self, request, id):
#         dentist = get_object_or_404(Dentist,pk= id)

#         patients = Appointment.objects.filter(dentist_id = id)

#         ss = PatientsSerializer(patients, many=True)

#         return Response(ss.data)


class GetAllPatientsView(ListAPIView):
    serializer_class = PatientsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        queryset = Appointment.objects.filter(dentist_id=dentist_id).distinct()
        return queryset


# TODO
# FETCH LIST OF PATIENTS THAT ARE ALREADY TREATED OR THE APPOINTMENT HAS PASSED
class GetTreatedPatientsView(ListAPIView):
    serializer_class = PatientsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id', None)
        queryset = Appointment.objects.filter(
            dentist_id=dentist_id).filter(available_at__lte=datetime.now())
        return queryset


# TODO
# FETCH LIST OF PATIENTS THAT ARE ALREADY TREATED OR THE APPOINTMENT HAS PASSED
# class GetPendingPatientsView(ListAPIView):
#     serializer_class = PatientsSerializer
#     pagination_class = PageNumberPagination

#     def get_queryset(self):
#         dentist_id = self.request.query_params.get('dentist_id',None)
#         queryset = Appointment.objects.filter(dentist_id=dentist_id).filter(available_at__gte=datetime.now())
#         return queryset


# Create your views here.


def index(request):
    return render(request, 'appointment/index.html')


def appointment_chat(request, appointment_chat_id):

    return render(request, 'appointment/room.html', {
        'chat_name': appointment_chat_id
    })
