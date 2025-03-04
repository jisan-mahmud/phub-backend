from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .paginations import CommentPagination
from django.db.models import Q, Count, Exists, OuterRef, Value, BooleanField
from .serializers import CommentSerializer
from .permission import CommentPermission
from .models import Comment
from votes.models import Vote

class CommentViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    pagination_class = CommentPagination

    def perform_create(self, serializer):
        snippet_id = self.kwargs.get('snippet_id') # store snippet id
        #set user_id and snippet_id in comment
        try:
            serializer.save(user= self.request.user, snippet_id= snippet_id)
        except:
            error_message = {
            "snippet": [
                "does not exist the specified snippet."
                ]
            }
            raise ValidationError(error_message)

    def get_queryset(self):
        user = self.request.user
        snippet_id = self.kwargs.get('snippet_id')
        is_root_only = self.request.query_params.get('root-comment') == 'true'


        if snippet_id and is_root_only:
            return Comment.objects.filter(snippet_id=snippet_id, parent_comment__isnull=True).select_related('user').annotate(
            is_voted =Exists(
                    Vote.objects.filter(comment=OuterRef('pk'), user= user)
                ) if user.is_authenticated else Value(False, output_field=BooleanField())
            )

        return Comment.objects.filter(snippet_id= snippet_id).select_related('user').annotate(
            is_voted =Exists(
                    Vote.objects.filter(comment=OuterRef('pk'), user= user)
                ) if user.is_authenticated else Value(False, output_field=BooleanField())
            )
    
    def get_serializer_context(self):
        # Add the request and snippet_id to the context
        context = super().get_serializer_context()
        context['request'] = self.request
        context['snippet_id'] = self.kwargs.get('snippet_id')
        return context

class CommentRepliesViewset(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def perform_create(self, serializer):
        snippet_id = self.kwargs.get('snippet_id')
        parent_comment_id = self.kwargs.get('parent_comment_id')  #store parent_comment id
        
        #set user_id and parent_comment in comment object
        try:
            serializer.save(user= self.request.user, parent_comment_id= parent_comment_id, snippet_id= snippet_id)
        except:
            error_message = {
            "parent_comment": [
                "the parent comment does not exist or does not belong to the specified snippet."
                ]
            }
            raise ValidationError(error_message)

    def get_queryset(self):
        snippet_id = self.kwargs.get('snippet_id')
        parent_comment_id = self.kwargs.get('parent_comment_id')
        comments = Comment.objects.filter(Q(parent_comment= parent_comment_id) & Q(snippet= snippet_id)).select_related('user')
        return comments
    
    def get_serializer_context(self):
        # Add the request to the context
        context = super().get_serializer_context()
        context['request'] = self.request 
        context['snippet_id'] = self.kwargs.get('snippet_id')
        return context