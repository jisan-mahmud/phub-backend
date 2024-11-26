from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, UserSnippetList, ShareUnlistedSnippetView, LoginUserSnippet

'''
This endpoint give all public snippet
Login user snippet
Loging user can post a snippet
'''
router = DefaultRouter()
router.register(r'', SnippetViewSet, basename= 'snippet')

urlpatterns = [
    path('my/', LoginUserSnippet.as_view(), name='login-user-snippet'),
    path('user/<str:username>/', UserSnippetList.as_view(), name='users-snippet'),
    path('share/<token>/', ShareUnlistedSnippetView.as_view(), name='share-unlisted-snappet'),

    # Snippet CRUD routes from router
    path('', include(router.urls)),
    
]
