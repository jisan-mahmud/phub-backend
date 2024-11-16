from rest_framework import serializers
from .models import Follow

class FollowSeralizer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ['followed', 'follower']

    def validate(self, attrs):
        follower = attrs.get('follower')
        followed = attrs.get('followed')

        print(followed, follower)
        # Check if a user is trying to follow themselves
        if follower == followed:
            raise serializers.ValidationError('You cannot follow yourself.')
        has = Follow.objects.filter(followed= followed, follower= follower).exists();

        if has:
            raise serializers.ValidationError('You are already following this user.')
        
        return attrs