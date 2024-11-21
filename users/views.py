from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
