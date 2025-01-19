from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .serializers import VoteSerializers
from .models import Vote
from django.core.cache import cache

class VoteViewset(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializers
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'

    def create(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')
        user = self.request.user

        # Validate the request data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Determine the vote type
        vote_type = serializer.validated_data.get('vote_type')

        # Function to handle voting logic
        def handle_vote(model_field, id):
            try:
                # Attempt to retrieve an existing vote
                if model_field == 'snippet_vote':
                    existing_vote = Vote.objects.get(user=user, snippet_id=id)
                elif model_field == 'comment_vote':
                    existing_vote = Vote.objects.get(user=user, comment_id=id)

                # If the same vote type is requested, delete the existing vote (unvote)
                if existing_vote.vote_type == vote_type:
                    existing_vote.delete()
                    return Response({"message": "Vote removed."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    # If a different vote type is requested, update the existing vote
                    existing_vote.vote_type = vote_type
                    existing_vote.save()
                    # Serialize the updated vote instance
                    updated_serializer = self.get_serializer(existing_vote)
                    return Response(updated_serializer.data, status=status.HTTP_200_OK)

            except Vote.DoesNotExist:
                # If no existing vote, create a new one
                if model_field == 'snippet_vote':
                    serializer.save(user=user, snippet_id=id)
                elif model_field == 'comment_vote':
                    serializer.save(user=user, comment_id=id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Handle vote for snippet
        if snippet_id and not comment_id:
            return handle_vote('snippet_vote', snippet_id)

        # Handle vote for comment
        if comment_id:
            return handle_vote('comment_vote', comment_id)

        return Response({"error": "Invalid vote data."}, status=status.HTTP_400_BAD_REQUEST)
            
            
    def retrieve(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')

        '''
        check this vote for snippet or comment.
        if this vote for exicute first one 'if block'
        if this vote for comment exicute 'elif block'
        '''

        # Default response message
        message = {"is_voted": False, "vote_type": None}

        if snippet_id and not comment_id:
            cache_key = f'snippet_vote:{snippet_id}'
            cache_data = cache.get(cache_key)
            if cache_data:
                return Response(cache_data, status= status.HTTP_200_OK)
            else:
                try:
                    vote = Vote.objects.get(user= request.user, snippet_id= snippet_id)
                    message = {
                        'is_voted': True,
                        'vote_type': vote.vote_type,
                        'snippet_id': vote.snippet.id  # Extract only the snippet ID
                    }
                    return Response(message, status= status.HTTP_200_OK)
                except Vote.DoesNotExist:
                    return Response(message, status= status.HTTP_200_OK)
                finally:
                    cache.set(cache_key, message, timeout= 500)


        elif comment_id:
            cache_key = f'comment_vote:{comment_id}'
            cache_data = cache.get(cache_key)
            if cache_data:
                return Response(cache_data, status= status.HTTP_200_OK)
            else:
                try:
                    vote = Vote.objects.get(user= request.user, comment_id= comment_id)
                    message = {
                        'is_voted': True,
                        'vote_type': vote.vote_type,
                        'snippet_id': vote.comment.id  # Extract only the snippet ID
                    }
                    cache.set(cache_key, message, timeout= 500)
                except Vote.DoesNotExist:
                    return Response(status= status.HTTP_204_NO_CONTENT)
    

    def destroy(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')

        '''
        check this vote for snippet or comment.
        if this vote for exicute first one 'if block'
        if this vote for comment exicute 'elif block'
        '''
        if snippet_id and not comment_id:
            vote = Vote.objects.filter(user= request.user, snippet_id= snippet_id).first()
        elif comment_id:
            vote = Vote.objects.filter(user= request.user, comment_id= comment_id).first()
        
        if vote:
            vote.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)