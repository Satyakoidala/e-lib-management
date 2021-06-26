from django.urls import path

from .views import *

app_name = 'users'

urlpatterns = [
    path('', loginview, name='login-view'),
    path('login/', validationview, name='user-validation-view'),
    path('forgot-password/', forgotpasswordview, name='forgot-password-view'),
    path('set-password/', setpasswordview, name='set-password-view'),
    path('set-password/update/', updatepasswordview, name='update-password-view'),
    path('view-profile/', viewprofileview, name='view-profile-view'),
    path('search/', searchresultview, name='search-result-view'),
    path('forgot-password/send-otp/', sendotpview, name="send-otp-view"),
    path('forgot-password/resend-otp/', resendotpview, name="resend-otp-view"),
    path('forgot-password/verify-otp/', verifyotpview, name="verify-otp-view"),
    path('logout', logoutview, name="logout-view"),
]
