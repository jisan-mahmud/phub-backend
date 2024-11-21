from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Follow
from .serializers import FollowSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserInformationSerializer
from rest_framework.permissions import AllowAny

User = get_user_model()


class UserAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username= None):
        if username:
            try:
                # Fetch the user from the database
                user = User.objects.get(username=username)
                serializer = UserInformationSerializer(user, context={'request': request})
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            user = User.objects.all()
            serializer = UserSerializer(user, many= True, context={'request': request})
        return Response(serializer.data)

class FollowCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request, username=None):
        # Try to find the user with the given username
        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            # If the user doesn't exist, return a 404 response with an error message
            return Response(
                {'error': f'User with username {username} does not exist.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = FollowSerializer(data={'followed': followed_user.id, 'follower': request.user.id})

        # Check if the serialized data is valid
        if serializer.is_valid():
            print('called')
            serializer.save(follower=request.user, followed=followed_user)
            return Response(
                {'message': 'Follow relationship created successfully.'},
                status=status.HTTP_201_CREATED
            )
        
        # If the data is invalid, return a 400 response with the validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, username= None):
        try:
            # Attempt to fetch the user object corresponding to the provided username
            followed_user = User.objects.get(username= username)
        except User.DoesNotExist:
            # If the user does not exist, return a 404 response with an error message
            return Response(
                {'error': f'User with username {username} does not exist.'}, 
                status= status.HTTP_404_NOT_FOUND
                )
        # Check if the authenticated user (follower) is already following the user (followed_user)
        already_followed = Follow.objects.filter(followed = followed_user, follower= request.user).exists()

        # Return a response indicating whether the user is already followed
        return Response({'already_followed': already_followed})