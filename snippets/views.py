from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Snippet
from .serializers import SnippetSerializer
from .permissions import SnippetPermission

class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    permission_classes = [AllowAny, SnippetPermission]
    serializer_class = SnippetSerializer

    def perform_create(self, serializer):
        # Automatically set the user to the currently authenticated user
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Snippet.objects.filter(
                Q(user = user) |
                Q(visibility = 'public')
                )
        return Snippet.objects.filter(visibility = 'public')

    
class UserSnippetList(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request, username):
        queryset = Snippet.objects.filter(user__username=username)
        serializer = SnippetSerializer(queryset, many=True)
        return Response(serializer.data)