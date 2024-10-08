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
    path('me/', LoginUserSnippet.as_view(), name='login-user-snippet'),
    path('user/<str:username>/', UserSnippetList.as_view({'get': 'list'}), name='users-snippet'),
    path('share/<token>/', ShareUnlistedSnippetView.as_view(), name='share-unlisted-snappet'),
    path('', include(router.urls)),
    
]
