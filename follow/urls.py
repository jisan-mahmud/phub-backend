from django.urls import path 
from .views import FollowCreateView

urlpatterns = [
    path('', FollowCreateView.as_view(), name= 'follow')
]
