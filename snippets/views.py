from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Exists, OuterRef
from .models import Snippet
from .serializers import SnippetSerializer
from .permissions import SnippetPermission
from .paginations import SnippetPagination
from votes.models import Vote

# ViewSet to handle all snippets operations
class SnippetViewSet(ModelViewSet):
    queryset = Snippet.objects.all()
    permission_classes = [SnippetPermission]
    serializer_class = SnippetSerializer
    pagination_class = SnippetPagination
    filterset_fields = ['language', 'title', 'created_at']
    ordering_fields = ['title', 'language', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user  # Get the current user making the request
        if user.is_authenticated:
            # If authenticated, return snippets that either belong to the user or are public
            return Snippet.objects.annotate(
                is_voted = Exists(
                    Vote.objects.filter(
                        user= user,
                        snippet= OuterRef('pk'),
                        comment__isnull= True
                    )
                )
            ).filter(
                Q(user = user) | # Snippets created by the current user
                Q(visibility = 'public') # Publicly visible snippets
            ).select_related('user')
        return Snippet.objects.filter(visibility = 'public').select_related('user')

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

# ViewSet to list all snippets belonging to a specific user by their username
class UserSnippetList(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = SnippetPagination
    serializer_class = SnippetSerializer

    def get_queryset(self):
        username = self.kwargs.get('username')
        if username:
            return Snippet.objects.filter(
            Q(user__username= username) &
            Q(visibility= 'public')
            ).select_related('user')
        return Snippet.objects.none
        
#This APIView for get login user snippet
class LoginUserSnippet(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = SnippetPagination
    serializer_class = SnippetSerializer
    def get_queryset(self):
        return Snippet.objects.filter(user= self.request.user).select_related('user')
    
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
