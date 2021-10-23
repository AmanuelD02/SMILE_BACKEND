from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from .models import Review, ReviewLike
from .serializers import ReviewLikeSerializer, ReviewSerializer

# Create your views here.


class ReviewView(APIView):
    def post(self, request):
        serializer = ReviewSerializer(data= request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST) 



    


class ReviewDetailView(APIView):
    ## dont forget pagination
    def get(self, request, review_id : int):
        review = get_object_or_404(Review, pk=review_id)
        serialize = ReviewSerializer(review)

        return Response(serialize.data)
        

    def delete(self, request, review_id : int):
        review = get_object_or_404(Review, pk=review_id)
        review.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)



class ReviewLikeListView(ListAPIView):
    serializer_class = ReviewLikeSerializer
    pagination_class = PageNumberPagination
    def get_queryset(self):
        review_id = self.request.query_params.get('review_id')
        queryset = ReviewLike.objects.filter(review_id=review_id)
        return queryset




class ReviewLikeView(APIView):
    # you get number of likes for a review
    def get(self, request, review_id: int):
        queryset = get_object_or_404(ReviewLike, review_id=review_id)
        serialize = ReviewLikeSerializer(queryset, many=True)

        return Response(serialize.data)

    # like a post
    def post(self, request, review_id: int):
        serializer = ReviewLikeSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # unlike a post
    def delete(self, request, review_id: int):
        serializer = ReviewLikeSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        # like = serializer.data

        like = get_object_or_404(ReviewLike, review_id = review_id, user_id = serializer.data.user_id)
        like.delete()

        return Response(status= status.HTTP_204_NO_CONTENT)

