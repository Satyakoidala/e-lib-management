from django.urls import path, include

from .views import *

app_name = 'student'

urlpatterns = [
    path('home/', homepageview, name='home-page-view'),
]
