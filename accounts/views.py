from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UserSerializer, UsernameSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status

User = get_user_model()
class UserAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, username= None):
        if username:
            try:
                # Fetch the user from the database
                user = User.objects.get(username=username)
                serializer = UserSerializer(user)
            except User.DoesNotExist:
                return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
        else:
            user = User.objects.all()
            serializer = UserSerializer(user, many= True)
        return Response(serializer.data)
    
class UpdateUsernameAPIView(APIView):
    def put(self, request):
        user = request.user
        serializer = UsernameSerializer(request.user, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)