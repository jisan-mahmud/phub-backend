from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Exists, OuterRef, Case, When, Value, CharField, Subquery
import uuid
User = get_user_model()


class SnippetManager(models.Manager):
    def get_user_voted_snippets(self, user):
        from votes.models import Vote
        """Returns all snippets along with whether the user has voted on them."""
        
         # Define the base query for checking user votes
        vote_filter = Vote.objects.filter(
            user=user,
            snippet= OuterRef('pk'),
            comment__isnull=True
        )
        
        return self.annotate(
            is_voted=Exists(vote_filter),
            vote_type=Case(
                When(is_voted=True, then= Subquery(vote_filter.values('vote_type')[:1])  # Grab only the first matching vote_type
                ),
                default=Value('no_vote'),
                output_field=CharField()
            )
        )

class Snippet(models.Model):
    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('c', 'C'),
        ('cpp', 'C++'),
        ('ruby', 'Ruby'),
        ('php', 'PHP'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('go', 'Go'),
        ('swift', 'Swift'),
    ]
    
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
        ('unlisted', 'Unlisted'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    snippet = models.TextField()
    language = models.CharField(max_length=15, choices=LANGUAGE_CHOICES)
    explanation = models.TextField(blank=True, null=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique= True, blank= True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    comment_count = models.PositiveIntegerField(default= 0)

    objects = SnippetManager()

    @property
    def total_comment(self):
        return self.total_comment
    

    def __str__(self):
        return f'id: {self.id}, title: {self.title}, create_by: {self.user}'

