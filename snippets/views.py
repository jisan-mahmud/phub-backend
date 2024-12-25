from django.core.cache import cache
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
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


    @method_decorator(cache_page(5))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        snippet_id = kwargs.get('pk')

        # Define cache keys
        snippet_cache_key = f'snippet:{snippet_id}'
        vote_cache_key = f'snippet_vote:{snippet_id}'

        # Fetch snippet data from cache
        snippet_cache_data = cache.get(snippet_cache_key)
        if snippet_cache_data is None:
            # Retrieve snippet data using the parent retrieve method
            response = super().retrieve(request, *args, **kwargs)
            snippet_cache_data = response.data
            cache.set(snippet_cache_key, snippet_cache_data, timeout= 60 * 5)

        # Fetch vote data from cache
        vote_cache_data = cache.get(vote_cache_key)
        if vote_cache_data is None:
            # Retrieve vote information from the database
            try:
                vote = Vote.objects.get(user=request.user, snippet_id=snippet_id)
                vote_cache_data = {
                    'is_voted': True,
                    'vote_type': vote.vote_type,
                    'snippet_id': snippet_id,
                }
            except Vote.DoesNotExist:
                vote_cache_data = {
                    'is_voted': False,
                    'vote_type': None,
                    'snippet_id': None,
                }
            cache.set(vote_cache_key, vote_cache_data, timeout= 60 * 5)

        # Combine snippet and vote data
        response_data = {**snippet_cache_data, **vote_cache_data}

        return Response(response_data, status=status.HTTP_200_OK)


    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user  # Get the current user making the request
        if user.is_authenticated:
            # If authenticated, return snippets that either belong to the user or are public
            snippets = Snippet.objects.get_user_voted_snippets(user).filter(
                Q(user = user) | # Snippets created by the current user
                Q(visibility = 'public') # Publicly visible snippets
            ).select_related('user')
            return snippets
        return Snippet.objects.filter(visibility = 'public').select_related('user')

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = {'request': self.request}
        return super().get_serializer(*args, **kwargs)

# ViewSet to list all snippets belonging to a specific user by their username
class UserSnippetList(ListAPIView):
    permission_classes = [AllowAny]
    pagination_class = SnippetPagination
    serializer_class = SnippetSerializer
    
    def get_paginated_response(self, data):
        print(data)
        return super().get_paginated_response(data)


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
