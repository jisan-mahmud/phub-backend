from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from .serializers import VoteSerializers
from .models import Vote

class VoteViewset(CreateAPIView, RetrieveAPIView, DestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializers
    lookup_field = 'id'

    def perform_create(self, serializer):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')
        user = self.request.user

        # Determine the vote type
        vote_type = serializer.validated_data.get('vote_type')

        # Function to handle voting logic
        def handle_vote(model_field, id):
            try:
                # Attempt to retrieve an existing vote
                if model_field == 'snippet_vote':
                    existing_vote = Vote.objects.get(user=user, snippet_id= id)
                elif model_field == 'comment_vote':
                    existing_vote = Vote.objects.get(user=user, comment_id= id)
                
                # If the same vote type is requested, delete the existing vote
                if existing_vote.vote_type == vote_type:
                    existing_vote.delete()
                    return True
                else:
                    # If a different vote type is requested, update the existing vote
                    existing_vote.vote_type = vote_type
                    existing_vote.save()

            except Vote.DoesNotExist:
                # If no existing vote, create a new one
                if model_field == 'snippet_vote':
                    serializer.save(user=user, snippet_id= id)
                elif model_field == 'comment_vote':
                    serializer.save(user=user, comment_id= id)

        # Handle vote for snippet
        if snippet_id and not comment_id:
            handle_vote('snippet_vote', snippet_id)

        # Handle vote for comment
        if comment_id:
            handle_vote('comment_vote', comment_id)
            

    def retrieve(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')
        if snippet_id and not comment_id:
            try:
                vote = Vote.objects.get(user= request.user, snippet_id= snippet_id)
            except Vote.DoesNotExist:
                return Response(status= status.HTTP_204_NO_CONTENT)
        elif comment_id:
            try:
                vote = Vote.objects.get(user= request.user, comment_id= comment_id)
            except Vote.DoesNotExist:
                return Response(status= status.HTTP_204_NO_CONTENT)
            
        seriaizer = self.get_serializer(vote)
        return Response(seriaizer.data, status= status.HTTP_200_OK)
    

    def destroy(self, request, *args, **kwargs):
        snippet_id = self.kwargs.get('snippet_id')
        comment_id = self.kwargs.get('comment_id')
        if snippet_id and not comment_id:
            vote = Vote.objects.filter(user= request.user, snippet_id= snippet_id).first()
        elif comment_id:
            vote = Vote.objects.filter(user= request.user, comment_id= comment_id).first()
        
        if vote:
            vote.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)