from rest_framework import serializers
from .models import Follow

class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['followed', 'follower']
        unique_together = ['followed', 'follower']

    def get_unique_together_validators(self):
        submited_data = self.initial_data
        if Follow.objects.filter(followed= submited_data.get('followed'), follower= submited_data.get('follower')).exists():
            raise serializers.ValidationError('Duplicate follow relationship detected.')
        return []
    
    
    def validate(self, attrs):
        followed = attrs.get('followed')
        follower = attrs.get('follower')

        if follower == followed:
            raise serializers.ValidationError('You cannot follow yourself.')
        
        return attrs