from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework import status
from .serializers import CommentSerializer
from .permission import CommentPermission
from .models import Comment

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def perform_create(self, serializer):
        
        #find snippet_id
        snippet_id = self.kwargs.get('snippet_id')

        #set user_id and snippet_id in comment
        serializer.save(user= self.request.user, snippet_id= snippet_id)

    def get_queryset(self):
        snippet_id = self.kwargs.get('snippet_id')
        comments = Comment.objects.filter(snippet_id=snippet_id).select_related('user')

        #check has comment for this snippet
        if comments.exists():
            return comments
        else:
            #raise not found error if not found comment
            raise NotFound("No comments found for this snippet.")

    def get_serializer_context(self):
        # Add the request to the context
        context = super().get_serializer_context()
        context['request'] = self.request 
        return context
    
    @action(detail=True, methods=['GET', 'POST'])
    def replies(self, request, pk=None):
        if request.method == 'GET':
            comment = self.get_object()
            replies = comment.replies.select_related('user')
            serializer = self.get_serializer(replies, many=True)
            return Response(serializer.data)

        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, parent_comment=self.get_object())  # Save the reply
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
