from django.contrib import admin
from .models import Snippet

class SnippetAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'visibility', 'user', 'created_at']
    ordering = ['created_at']
    search_fields = ['user', 'title']

    # readonly_fields = ['upvotes', 'downvotes']

admin.site.register(Snippet, SnippetAdmin)