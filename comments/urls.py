from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewset, CommentRepliesViewset

router = DefaultRouter()
router.register(r'', CommentViewset, basename='comments')
# router.register(r'<int:parent_comment>replies/', CommentRepliesViewset, basename='comment-replies')

urlpatterns = [
    path('<int:parent_comment_id>/replies/', CommentRepliesViewset.as_view({'get': 'list', 'post': 'create'}), name='comment-replies'),  # Use separate path for replies

    # Nested vote routes: include vote-related URLs under /comments/<comment_id>/vote/
    path('<int:comment_id>/vote/', include('votes.urls')),
    path('', include(router.urls)),
]
