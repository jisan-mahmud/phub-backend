from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .serializers import UsernameSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status

User = get_user_model()
    
class UpdateUsernameAPIView(APIView):
    def put(self, request):
        user = request.user
        serializer = UsernameSerializer(request.user, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status= status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)