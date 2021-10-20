from re import search
from django.shortcuts import get_object_or_404
from rest_framework import   status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from clinic.serializers import ClinicSerializer

from  .models import Clinic

# Create your views here.


class ClinicDetailView(APIView):
    def get(self, request, clinic_id):
        clinic = get_object_or_404(Clinic, pk= clinic_id)
        serializer = ClinicSerializer(clinic)
   
        return Response(serializer.data)
    
    def put(self, request, clinic_id):
        clinic = get_object_or_404(Clinic, pk= clinic_id)
        serializer = ClinicSerializer(clinic)
        serializer.update()

        return Response(serializer.data)

    def delete(self, request, clinic_id):
        clinic = get_object_or_404(Clinic, pk= clinic_id)
        serializer = ClinicSerializer(clinic)
        serializer.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)    
        
class ClinicView(APIView):
    def post(self, request):
        serializer = ClinicSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class ClinicSearchView(ListAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filter_backends= (SearchFilter, OrderingFilter)
    pagination_class = PageNumberPagination

    search_fields = ('name', 'bio')


