from django.urls import path, include
from .views import UserAPIView
from follow.views import UnfollowView

urlpatterns = [
    path('', UserAPIView.as_view(), name= "users"),
    path('<username>/', UserAPIView.as_view(), name= "user"),
    path('<username>/follow/', include('follow.urls')),
    path('<username>/unfollow/', UnfollowView.as_view(), name= 'user-unfollow')
]
