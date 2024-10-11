from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CommentViewset

router = DefaultRouter()
router.register(r'', CommentViewset, basename='snippet-comments')

urlpatterns = [
    path('', include(router.urls)),
]
