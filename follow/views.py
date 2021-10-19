from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Follow
from follow.serializers import FollowSerializer


# Create your views here.


class FollowView(APIView):
    def post(self, request):
        serializer = FollowSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)
    

    def put(self, request):
        serializer = FollowSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

        
    def delete(self, request):
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
            followers = FollowSerializer(queryset, many = True)
            return Response(followers.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    