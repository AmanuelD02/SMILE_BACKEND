
from django.shortcuts import get_object_or_404
from django.db import transaction

from rest_framework.response import Response
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from .models import Appointment, Availability, PendingAppointment
from .serializer import AppointmentMessageSerializer, AppointmentSerializer, AvailabiltySerializer, PendingAppointmentSerializer


# Create your views here.
class AvailabilityView(APIView):
    def post(self, request):
        serializer = AvailabiltySerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()



class AvailabilityDetailView(APIView):
    def get(self, request, availabilty_id):
        available = get_object_or_404(Availability, pk=availabilty_id)
        serializer = AvailabiltySerializer(available)
        
        return Response(serializer.data)

    def delete(self, request, availabilty_id):
        available = get_object_or_404(Availability, pk=availabilty_id)
        available.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

class  AvailabiltyListView(ListAPIView):
    serializer_class = AvailabiltySerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id',None)
        queryset = Availability.objects.filter(dentist_id=dentist_id)
        return queryset





class PendingAppointmentView(APIView):
    def post(self,request):
        serializer = PendingAppointmentSerializer(data = request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        available = Availability.objects.filter(available_at= serializer.data['available_at']).first()
        if available:
            serializer.save()
            return Response(serializer.data)
        
        return Response({"message":"Invalid Availability"},status=status.HTTP_400_BAD_REQUEST)

class PendingAppointmentDetailView(APIView):
    def get(self, request, pending_id):
        pending = get_object_or_404(PendingAppointment, pk=pending_id)
        serializer = PendingAppointmentSerializer(pending)
        return Response(serializer.data)
    

    def delete(self, request, pending_id):
        pending = get_object_or_404(PendingAppointment, pk=pending_id)
        pending.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)




class  PendingAppointmentListView(ListAPIView):
    serializer_class = PendingAppointment
    pagination_class = PageNumberPagination
    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id',None)
        queryset = PendingAppointment.objects.filter(dentist_id=dentist_id)
        return queryset

class AppointmentView(APIView):
    def post(self,request):
        serializer = AppointmentSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        available = Availability.objects.filter(avaialble_at= serializer.data['avaialble_at']).first()
        if available:
            with transaction.atomic():
                available.delete()
                pending = PendingAppointment.objects.filter(dentist_id = serializer.data['dentsit_id'], avaialble_at= serializer.data['avaialble_at']).first()
                pending.delete()
                serializer.save()
            return Response(serializer.data)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)
    


class AppointmentListView(ListAPIView):
    serializer_class = AppointmentView
    pagination_class = PageNumberPagination
    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id',None)
        user_id = self.request.query_params.get('user_id',None)
        queryset = Appointment.objects.filter(dentist_id=dentist_id,user_id = user_id )
        return queryset


class AppointmentDetailView(APIView):
    def get(self,request, appointment_id):
        appointment = get_object_or_404(Appointment, pk= appointment_id)

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data)

    def delete(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, pk= appointment_id)
        appointment.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)



class AppointmentMessagView(APIView):
    def post(self, request):
        serializer = AppointmentMessageSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    
class GetAppointmentMessageView(ListAPIView):
    serializer_class = AppointmentMessageSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        dentist_id = self.request.query_params.get('chat_id',None)
        queryset = PendingAppointment.objects.filter(dentist_id=dentist_id)
        return queryset.reverse()
    