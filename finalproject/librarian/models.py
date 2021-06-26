from django.db import models

# Create your models here.
from users.models import *


class Librarian(models.Model):
    libid = models.ForeignKey(
        Library_Users, related_name='librarians', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    issuedcount = models.IntegerField(default=0, blank=True)
    retrievedcount = models.IntegerField(default=0, blank=True)
    totalactions = models.IntegerField(default=0, blank=True)


class Dashboard(models.Model):
    totalbooks = models.IntegerField(default=0, blank=True)
    booksinside = models.IntegerField(default=0, blank=True)
    issuedbooks = models.IntegerField(default=0, blank=True)
    submittedbooks = models.IntegerField(default=0, blank=True)
