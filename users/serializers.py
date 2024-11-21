from rest_framework import serializers
from .models import Follow
from django.contrib.auth import get_user_model
from django.urls import reverse
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    profile_url = serializers.SerializerMethodField() 
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_image', 'profile_url']
        
    def get_profile_url(self, obj):
        # Construct and return the profile URL based on the user's ID
        relative_url = reverse('user', kwargs={'username': obj.username})
        return self.context['request'].build_absolute_uri(relative_url)

class UserInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'about', 'bio', 'profile_image', 'cover_image','followers', 'following', 'total_post']


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['followed', 'follower']
        unique_together = ['followed', 'follower']

    # Override the method to customize unique together validation
    def get_unique_together_validators(self):
        submited_data = self.initial_data
        # Check if a follow relationship already exists in the database
        if Follow.objects.filter(followed= submited_data.get('followed'), follower= submited_data.get('follower')).exists():
            raise serializers.ValidationError('Duplicate follow relationship detected.')
        return []
    
    # Additional validation logic for the serializer
    def validate(self, attrs):
        followed = attrs.get('followed')
        follower = attrs.get('follower')

        # Custom check to prevent a user from following themselves
        if follower == followed:
            raise serializers.ValidationError('You cannot follow yourself.')
        
        return attrs