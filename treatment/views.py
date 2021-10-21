from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers, status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView


from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import Treatment, TreatmentName

from .serializer import TreatmentNameSerializer, TreatmentSerializer

# Create your views here.


class TreatmentNameView(APIView):
    def post(self, request):
        serializer = TreatmentNameSerializer(data = request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()

        return Response(serializer.data)
    
class TreatmentNameListView(ListAPIView):
    queryset = TreatmentName.objects.all()
    serializer_class = TreatmentNameSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    pagination_class = PageNumberPagination

    search_fields = ('name')



class TreatmentNameDetailView(APIView):
    def get(self, request, treatment_name_id):
        treatment  = get_object_or_404(TreatmentName, pk=treatment_name_id)
        serializer = TreatmentNameSerializer(treatment)

        return Response(serializer.data)

    def put(self, request, treatment_name_id):
        treatment  = get_object_or_404(TreatmentName, pk=treatment_name_id)
        serializer = TreatmentNameSerializer(treatment,data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, treatment_name_id):
        treatment  = get_object_or_404(TreatmentName, pk= treatment_name_id)
        treatment.delete()

        return Response(status = status.HTTP_204_NO_CONTENT)

        



class TreatmentView(APIView):
    def post(self, request):
        serializer = TreatmentSerializer(data = request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

        
class TreatmentListView(ListAPIView):
    serializer_class = TreatmentSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id')
        queryset = Treatment.objects.filter(dentist_id=dentist_id)
        return queryset

class TreatmentDetailView(APIView):
    def get(self, request, treatment_id):
        treament = get_object_or_404(Treatment, pk= treatment_id)
        serializer = TreatmentSerializer(treament)
        
        return Response(serializer.data)

    def put(self, request, treatment_id):
        treatment = get_object_or_404(Treatment, pk= treatment_id)
        serializer = TreatmentSerializer(treatment,data = request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)



