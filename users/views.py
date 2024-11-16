from rest_framework.generics import CreateAPIView
from .models import Follow
from .serializers import FollowSeralizer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowCreateView(CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSeralizer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        username = self.kwargs['username']
        try:
            followed_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(f"User with username '{username}' does not exist.")
        serializer.save(followed= self.request.user, follower= followed_user)