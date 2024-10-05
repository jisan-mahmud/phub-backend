from django.db import models
from django.contrib.auth import get_user_model
from .language import detect_language

User = get_user_model()

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='snippets')
    title = models.CharField(max_length=250)
    description = models.TextField(blank=True)
    snippet = models.TextField()
    snippet_type = models.CharField(max_length=15, choices= LANGUAGE_CHOICES)
    explanation = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.title} by {self.user}'

