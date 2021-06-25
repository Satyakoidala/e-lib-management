from django.db import models

# Create your models here.

from users.models import *

class Students(models.Model):
    studid = models.ForeignKey(Library_Users, related_name='students', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    section = models.IntegerField(default=1, blank=False)
    academicyear = models.CharField(max_length=9, default='2017-2021', blank=False, null=False)
    amountpaid = models.IntegerField(default=0, blank=False)