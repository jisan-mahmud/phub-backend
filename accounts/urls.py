from django.urls import path, include
from .views import UserAPIView, UpdateUsernameAPIView

urlpatterns = [
    path('auth/users/update-username/', UpdateUsernameAPIView.as_view(), name= "username-update"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('users/', UserAPIView.as_view(), name= "users"),
    path('users/<username>/', UserAPIView.as_view(), name= "user"),
]
