from django.urls import path, include

from .views import *

app_name = 'librarian'

urlpatterns = [
    path('home/', homepageview, name='home-page-view'),

    path('student-profile/', studentprofileview, name='student-profile-view'),
]
