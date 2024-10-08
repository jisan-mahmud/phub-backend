from rest_framework import serializers
from django.urls import reverse
from .models import Snippet

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'user', 'title', 'description', 'snippet', 'language', 'created_at', 'last_update', 'upvotes', 'downvotes', 'visibility', 'token']
        read_only_fields = ['user']

    # overrite default serializer representation
    def to_representation(self, instance):
        data = super().to_representation(instance)

        #add important link
        data['link'] = {
            'visit': self.context['request'].build_absolute_uri(f'/api/snippets/{instance.id}/'),
        }

        #If request not equal to snippet onwer remove secret token
        if self.context['request'].user != instance.user:
            data.pop('token', None)
        return data