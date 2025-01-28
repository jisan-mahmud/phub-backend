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


class CurrentUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'bio', 'profile_image', 'cover_image', 'about', 'followers', 'following', 'total_post']

        extra_kwargs ={
            'email': {
                'read_only': True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        snippet_url = reverse('users-snippet', kwargs= {'username': instance.username})
        follow_url = reverse('follow', kwargs= {'username': instance.username})
        unfollow_url = reverse('user-unfollow', kwargs= {'username': instance.username})
        followers_url = reverse('follower-list', kwargs= {'username': instance.username})
        following_url = reverse('following-list', kwargs= {'username': instance.username})
    
        data['link'] = {
            'snippet': self.context['request'].build_absolute_uri(snippet_url),
            'follow': self.context['request'].build_absolute_uri(follow_url),
            'unfollow': self.context['request'].build_absolute_uri(unfollow_url),
            'follower': self.context['request'].build_absolute_uri(followers_url),
            'following': self.context['request'].build_absolute_uri(following_url),
        }

        return data


class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {
            'username': {
                'required': True,
            },
        }
