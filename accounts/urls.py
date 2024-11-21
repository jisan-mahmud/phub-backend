from django.urls import path, include
from .views import UpdateUsernameAPIView

urlpatterns = [
    path('auth/users/update-username/', UpdateUsernameAPIView.as_view(), name= "username-update"),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
