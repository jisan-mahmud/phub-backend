from django.urls import path
from .views import SingupAPIView
urlpatterns = [
    path('signup/', SingupAPIView.as_view(), name='sign_up'),
]
