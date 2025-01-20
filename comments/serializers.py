from rest_framework import serializers
from django.urls import reverse
from .models import Comment
from users.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    is_voted = serializers.BooleanField(default= False)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'last_modify', 'upvotes', 'downvotes', 'total_replies', 'is_voted']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        context = self.context
        snippet_id = context.get('snippet_id')

        data['links'] = {
            'self': context['request'].build_absolute_uri(reverse('comments-detail', args=[snippet_id, instance.id])),  # Link to view the comment detail
            'update': context['request'].build_absolute_uri(reverse('comments-detail', args=[snippet_id, instance.id])),  # Link to update the comment
            'delete': context['request'].build_absolute_uri(reverse('comments-detail', args=[snippet_id, instance.id])),  # Link to delete the comment
            'reply': context['request'].build_absolute_uri(reverse('comment-replies', args=[snippet_id, instance.id])),# Link to reply to the comment
            'vote': context['request'].build_absolute_uri(reverse('vote', kwargs= {'comment_id': instance.id}))
        }
        return data