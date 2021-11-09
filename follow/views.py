from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

from .serializers import FollowSerializer
from .models import Follow


# Create your views here.


class FollowView(APIView):
    def post(self, request):
        serializer = FollowSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        
        follow= Follow.objects.filter(user_id=serializer.validated_data['user_id'], dentist_id =serializer.validated_data['dentist_id'] )
        
        if follow:
            return Response( serializer.data,status=status.HTTP_409_CONFLICT)


        serializer.save()

        return Response(serializer.data)
    

    def put(self, request):
        follower = Follow.objects.filter(dentist_id=request.data['dentist_id'], user_id=request.data['user_id']).first()
        if follower ==None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = FollowSerializer(follower,data= request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

        
    def delete(self, request):
        serializer = FollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            follow = Follow.objects.filter(dentist_id = request.data['dentist_id'], user_id = request.data['user_id']).first()
            follow.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        




class FollowDetailView(APIView):
    def get(self, request, dentist_id: int):
        try:
            queryset = Follow.options.filter(dentist_id=dentist_id)
            followers = FollowSerializer(data=queryset, many = True)
            return Response(followers.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class FollowDetailListView(ListAPIView):
    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        dentist_id = self.request.query_params.get('dentist_id',None)
        queryset = Follow.objects.filter(dentist_id=dentist_id)
        return queryset
