from django.db import models
from django.db.models import Q
from snippets.models import Snippet
from comments.models import Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class Vote(models.Model):
    VOTE_TYPE = (
       ('upvote', 'Upvote'),
       ('downvote', 'Downvote')
    )
    user = models.ForeignKey(User, models.CASCADE, related_name= 'votes')
    snippet = models.ForeignKey(Snippet, models.CASCADE, related_name= 'snippet_votes', blank= True, null= True)
    comment = models.ForeignKey(Comment, models.CASCADE, related_name= 'comment_votes', blank= True, null= True)
    vote_type = models.TextField(max_length=10, choices= VOTE_TYPE)
    created_at = models.DateTimeField(auto_now_add= True)

    class Meta:
        constraints = [
            # Ensuring that a vote is made either on a snippet or a comment, not both
            models.CheckConstraint(
                check=(Q(snippet__isnull=False) & Q(comment__isnull=True)) | (Q(snippet__isnull=True) & Q(comment__isnull=False)),
                name= 'vote_snippet_or_commnet'
            ),
            # Enforce unique vote per user for each snippet
            models.UniqueConstraint(
                fields= ['user', 'snippet'],
                name= 'unique_user_snippet',
                condition= Q(snippet__isnull= False)
            ),
            # Enforce unique vote per user for each comment
            models.UniqueConstraint(
                fields= ['user', 'comment'],
                name= 'unique_user_comment',
                condition= Q(comment__isnull= False)
            )
        ]

    def __str__(self) -> str:
        return f'vote type- {self.vote_type}'