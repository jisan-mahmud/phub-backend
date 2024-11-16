from rest_framework.serializers import ModelSerializer
from .models import Follow

class FollowSeralizer(ModelSerializer):

    class Meta:
        model = Follow
        fields = ['followed', 'follower']

        extra_kwargs = {
            'followed': {
                'read_only': True
            },
            'follower': {
                'read_only': True
            }
        }