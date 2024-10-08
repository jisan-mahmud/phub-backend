from django.db.models import Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Snippet
from .serializers import SnippetSerializer
from .permissions import SnippetPermission

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    permission_classes = [SnippetPermission]
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user  # Get the current user making the request
        if user.is_authenticated:
            # If authenticated, return snippets that either belong to the user or are public
            return Snippet.objects.filter(
                Q(user = user) | # Snippets created by the current user
                Q(visibility = 'public') # Publicly visible snippets
                )
        return Snippet.objects.filter(visibility = 'public')

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

# ViewSet to list all snippets belonging to a specific user by their username
class UserSnippetList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request, username):
        queryset = Snippet.objects.filter(
            Q(user__username=username) &
            Q(visibility= 'public')
            )
        serializer = SnippetSerializer(queryset, many=True, context= {'request': request})
        return Response(serializer.data, status= status.HTTP_200_OK)
    
#This APIView for get login user snippet
class LoginUserSnippet(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        snippet = Snippet.objects.filter(user= request.user)
        if snippet.exists():
            serializer = SnippetSerializer(snippet, many= True, context= {'request': request})
            return Response(serializer.data, status= status.HTTP_200_OK)
        return Response(status= status.HTTP_204_NO_CONTENT)
    
# Define a ViewSet class to handle sharing unlisted snippets
class ShareUnlistedSnippetView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            # Get the snippet object that matches the provided token
            snippet = get_object_or_404(Snippet, token=token)
            serializer = SnippetSerializer(snippet, context={'request': request})
            return Response(serializer.data, status= status.HTTP_200_OK)
        except Exception as e:
            return Response(status= status.HTTP_404_NOT_FOUND)
