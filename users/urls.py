from django.urls import path, include
from .views import UserAPIView
from follow.views import FollowView, UnfollowView, FollowerList, FollowingList

urlpatterns = [
    path('', UserAPIView.as_view(), name= "users"),
    path('<username>/', UserAPIView.as_view(), name= "user"),
    path('<username>/follow/', FollowView.as_view(), name= 'follow'),
    path('<username>/unfollow/', UnfollowView.as_view(), name= 'user-unfollow'),
    path('<username>/follower-list/', FollowerList.as_view(), name= 'follower-list'),
    path('<username>/following-list/', FollowingList.as_view(), name= 'following-list')
]
