from users.views import forgotpasswordview
from django.urls import path, include

from .views import *

app_name = 'users'

urlpatterns = [
    path('', loginview, name='login-view'),
    path('forgot-password/', forgotpasswordview, name='forgot-password-view'),
    path('set-password/', setpasswordview, name='set-password-view'),
    path('view-profile/', viewprofileview, name='view-profile-view'),
    path('search/', searchresultview, name='search-result-view'),
]
