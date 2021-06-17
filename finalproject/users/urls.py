from django.urls import path, include

from .views import *

app_name = 'users'

urlpatterns = [
    path('', loginview, name='login-view'),
]