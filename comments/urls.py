from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewset, CommentRepliesViewset

# Create a single router for comments
router = DefaultRouter()

# Register the common CommentViewset for general comment operations
router.register(r'', CommentViewset, basename='comments')

urlpatterns = [
    # Base comment URL (GET, POST, DELETE, UPDATE for all comments)
    path('', include(router.urls)),
    # Snippet-specific comment URLs (with snippet_id)
    path('snippets/<int:snippet_id>/comments/', CommentViewset.as_view({'get': 'list', 'post': 'create'}), name='snippet-comments'),
    # Nested route for replies to a specific comment
    path('<int:comment_id>/replies/', CommentRepliesViewset.as_view({'get': 'list', 'post': 'create'}), name='comment-replies'),

    # Path for voting on a specific comment
    path('comments/<int:comment_id>/vote/', include('votes.urls')),
]
