from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import SignupSerializer

class SingupAPIView(APIView):
    def post(self, request, formate= None):
        user_serializer = SignupSerializer(data= request.data)

        if user_serializer.is_valid():
            return Response(user_serializer.data, status= status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        