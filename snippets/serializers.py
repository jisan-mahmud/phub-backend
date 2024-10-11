from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snippet
from accounts.serializers import UserSerializer
User = get_user_model()


class SnippetSerializer(serializers.ModelSerializer):
    # Nesting user serializer with snippet serializer
    user = UserSerializer(read_only= True)
    class Meta:
        model = Snippet
        fields = ['id', 'user', 'title', 'description', 'snippet', 'language', 'created_at', 'last_update', 'upvotes', 'downvotes', 'visibility', 'token']

    # overrite default serializer representation
    def to_representation(self, instance):
        print(self.context['request'].build_absolute_uri())
        data = super().to_representation(instance)

        #add important link
        data['link'] = {
            'visit': self.context['request'].build_absolute_uri(f'{instance.id}/'),
        }

        #If request not equal to snippet onwer remove secret token
        if self.context['request'].user != instance.user:
            data.pop('token', None)
        return data