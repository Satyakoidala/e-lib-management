from django.urls import path, include

from .views import *

app_name = 'librarian'

urlpatterns = [
    path('home/', homepageview, name='home-page-view'),
    path('home/student-profile/', studentprofileview, name='student-profile-view'),
    path('home/issue-book/', issuebookview, name='issue-book-view'),
    path('home/submit-book/', submitbookview, name='submit-book-view'),
    path('send-notifications/', sendnotificationsview, name='send-notifications-view'),
]
