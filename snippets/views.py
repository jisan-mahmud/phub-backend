from django.shortcuts import render
from rest_framework import viewsets
from .models import Snippet

class SnippetViewset(viewsets):
    