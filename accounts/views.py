from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer
from django.contrib.auth import get_user_model
User = get_user_model()

class SingupAPIView(APIView):
    def post(self, request, formate= None):
        serializer = SignupSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        