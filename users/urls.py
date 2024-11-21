from django.urls import path
from .views import UserAPIView, FollowCreateView

urlpatterns = [
    path('', UserAPIView.as_view(), name= "users"),
    path('<username>/', UserAPIView.as_view(), name= "user"),
    path('<username>/follow/', FollowCreateView.as_view(), name= 'follow')
]
