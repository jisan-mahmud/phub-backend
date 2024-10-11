from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(max_length=100, write_only=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'repeat_password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('repeat_password')
        username = validated_data.get('email').split('@')[0]
        user = User(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.is_active = False
        user.username = username
        user.save()

        return user

#user information in long formate
class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'bio', 'profile_image', 'cover_image', 'about', 'followers', 'following', 'total_post']

class CurrentUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'bio', 'profile_image', 'cover_image', 'about', 'followers', 'following', 'total_post']

        extra_kwargs ={
            'email': {
                'required': False
            }
        }


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {
            'username': {
                'required': True,
            },
        }

# User information in short form
class UserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_image', 'profile_url']
        
    def get_profile_url(self, obj):
        # Construct and return the profile URL based on the user's ID
        relative_url = reverse('user', kwargs={'username': obj.username})
        return self.context['request'].build_absolute_uri(relative_url)