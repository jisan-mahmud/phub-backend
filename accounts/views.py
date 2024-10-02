from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.response import Response
from .serializers import SignupSerializer
User = get_user_model()

class SingupAPIView(APIView):
    
    permission_classes = [AllowAny]
    def post(self, request, formate= None):
        serializer = SignupSerializer(data= request.data, context= {'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response({'errors': serializer.errors}, status= status.HTTP_400_BAD_REQUEST)


def verify_email(request):
    token = request.GET.get('token')

    if not token:
        return JsonResponse({'error': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        access_token = AccessToken(token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)
        if user.is_active:
            return JsonResponse({'detail': 'User already verified'}, status=status.HTTP_200_OK)

        # Activate the user
        user.is_active = True
        user.save()

        return JsonResponse({'detail': 'Email successfully verified'}, status=status.HTTP_200_OK)

    except TokenError:
        return JsonResponse({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)