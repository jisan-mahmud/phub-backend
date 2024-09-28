from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length= 100)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']
