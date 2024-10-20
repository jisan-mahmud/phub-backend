from rest_framework.serializers import ModelSerializer
from .models import Vote

class VoteSerializers(ModelSerializer):
    class Meta:
        model = Vote
        fields= ['user', 'snippet', 'comment', 'vote_type', 'created_at']
        extra_kwargs = {
            'user': {
                'read_only': True,
            },
            'snippet': {
                'read_only': True,
            },
            'comment': {
                'read_only': True,
            }
        }