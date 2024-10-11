from django.db import models
from django.core.exceptions import ValidationError
from snippets.models import Snippet
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def clean(self):
        # Ensure that either parent_comment or snippet is provided, but not both
        if not self.parent_comment and not self.snippet:
            raise ValidationError('You must provide either a parent comment or a snippet.')
        if self.parent_comment and self.snippet:
            raise ValidationError('You cannot provide both a parent comment and a snippet.')
        # Ensure that a comment cannot be its own parent
        if self.parent_comment == self:
            raise ValidationError('A comment cannot reply to itself.')

    def __str__(self) -> str:
        return f'{self.id} comment by {self.user}'