from django.urls import path, include

from .views import *

app_name = 'student'

urlpatterns = [
    path('home/', homepageview, name='home-page-view'),
    path('home/pay/<int:bookid>/', paymentview, name='payment-view'),
    path('home/pay/<int:bookid>/success/',
         paymentsuccessview, name='payment-success-view'),
    path('home/pay/<int:bookid>/failure/',
         paymentfailureview, name='payment-failure-view'),
]
