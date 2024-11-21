from rest_framework import serializers
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
    snippets = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'about', 'bio', 'profile_image', 'cover_image','followers', 'following', 'total_post', 'snippets']
    
    def get_snippets(self, obj):
        snippet_url = reverse('users-snippet', kwargs= {'username': obj.username})
        return self.context['request'].build_absolute_uri(snippet_url)
