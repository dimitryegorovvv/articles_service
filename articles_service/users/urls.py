from django.urls import path, include
from .views import *

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', register_page, name='register_page'),
    path('register/user/', register, name='register'),
]