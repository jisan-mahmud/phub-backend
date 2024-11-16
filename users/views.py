from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from .serializers import FollowSeralizer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

User = get_user_model()

class FollowCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, username= None):

        try:
            followed_user = User.objects.get(username= username)
        except User.DoesNotExist:
            return Response(
                {'error': f'User with username {username} does not exist.'}, 
                status= status.HTTP_404_NOT_FOUND
                )
        
        data = {
            'followed': followed_user.id,
            'follower': request.user.id
        }
        
        serializer = FollowSeralizer(data= data)

        if serializer.is_valid():
            serializer.save(follower=request.user, followed=followed_user)
            return Response(
                {'message': 'Follow relationship created successfully.'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username= None):
        try:
            followed_user = User.objects.get(username= username)
        except User.DoesNotExist:
            return Response(
                {'error': f'User with username {username} does not exist.'}, 
                status= status.HTTP_404_NOT_FOUND
                )
        already_followed = Follow.objects.filter(followed = followed_user, follower= request.user).exists()

        return Response({'already_followed': already_followed})