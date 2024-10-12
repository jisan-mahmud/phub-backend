from django.db import models
from django.core.exceptions import ValidationError
from snippets.models import Snippet
from django.contrib.auth import get_user_model

User = get_user_model()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    snippet = models.ForeignKey(Snippet, on_delete=models.CASCADE, related_name='comments')
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_modify = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    reply_count = models.PositiveIntegerField(default= 0)

    @property
    def total_replies(self):
        return self.reply_count
    
    def clean(self):
        if self.parent_comment == self:
            raise ValidationError('A comment cannot reply to itself.')
        
        # Ensure the snippet of the comment matches the snippet of its parent comment
        if self.parent_comment and self.snippet != self.parent_comment.snippet:
            raise ValidationError('The comment\'s snippet must match the parent comment\'s snippet.')

    def __str__(self) -> str:
        return f'{self.id} comment by {self.user}'