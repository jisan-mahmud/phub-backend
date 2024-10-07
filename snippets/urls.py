from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SnippetViewSet, UserSnippetList

'''
This endpoint give all public snippet
Login user snippet
Loging user can post a snippet
'''
router = DefaultRouter()
router.register(r'', SnippetViewSet, basename= 'snippet')

urlpatterns = [
    path('user/<str:username>/', UserSnippetList.as_view({'get': 'list'}), name='users-snippet'),
    path('', include(router.urls)),
    
]
