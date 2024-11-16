from django.urls import path
from .views import FollowCreateView
urlpatterns = [
    path('<username>/follow/', FollowCreateView.as_view(), name= 'follow')
]
