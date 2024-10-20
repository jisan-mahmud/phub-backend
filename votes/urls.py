from django.urls import path, include
from .views import VoteViewset

urlpatterns = [
    path('', VoteViewset.as_view(), name= 'vote'),
]
