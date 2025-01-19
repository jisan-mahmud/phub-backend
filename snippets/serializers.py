from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Snippet
from users.serializers import UserSerializer
User = get_user_model()


class SnippetSerializer(serializers.ModelSerializer):
    # Nesting user serializer with snippet serializer
    user = UserSerializer(read_only= True)

    class Meta:
        model = Snippet
        fields = ['id', 'user', 'title', 'description', 'snippet', 'language', 'created_at', 'last_update', 'upvotes', 'downvotes', 'total_comment', 'visibility', 'token']

    # overrite default serializer representation
    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # add important link
        data['link'] = {
            'self': self.context['request'].build_absolute_uri(f'{instance.id}/'),
            'update': self.context['request'].build_absolute_uri(f'{instance.id}/'),
            'delete': self.context['request'].build_absolute_uri(f'{instance.id}/'),
            'comments': self.context['request'].build_absolute_uri(reverse('comments-list', args=[instance.id])) + '?root-comment=true',
            'vote': self.context['request'].build_absolute_uri(reverse('vote', args= [instance.id])),
        }

        #If request not equal to snippet onwer remove secret token
        if self.context['request'].user != instance.user:
            data.pop('token', None)
        return data