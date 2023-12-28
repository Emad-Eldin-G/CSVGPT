from django.urls import path
from .views import *

urlpatterns = [
    path('sendPrompt/', sendPrompt, name='sendPrompt'),
]