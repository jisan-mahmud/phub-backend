from django.urls import path
from .views import FollowCreateView
from rest_framework.routers import DefaultRouter
urlpatterns = [
    path('<username>/follow/', FollowCreateView.as_view(), name= 'follow')
]
