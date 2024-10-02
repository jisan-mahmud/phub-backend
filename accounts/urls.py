from django.urls import path
from .views import SingupAPIView, verify_email
urlpatterns = [
    path('signup/', SingupAPIView.as_view(), name='sign_up'),
    path('verify-email/', verify_email, name='verify-email')
]
