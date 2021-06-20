from django.db import models

# Create your models here.
class Library_Users(models.Model):
    userid = models.CharField(max_length=10, blank=False, null=False)
    password = models.CharField(max_length=15, blank=False, null=False)
    name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    isLibrarian = models.BooleanField(blank=False, null=False)

class Issued_Books(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    stud_id = models.CharField(max_length=10, blank=False, null=False)
    lib_id = models.CharField(max_length=10, blank=False, null=False)
    bookid = models.CharField(max_length=5, blank=False, null=False)
    duedate = models.DateField(auto_now=False, auto_now_add=False)
    amount_due = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)

class Submitted_Books(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    stud_id = models.CharField(max_length=10, blank=False, null=False)
    lib_id = models.CharField(max_length=10, blank=False, null=False)
    bookid = models.CharField(max_length=5, blank=False, null=False)

class History(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    stud_id = models.CharField(max_length=10, blank=False, null=False)
    lib_id = models.CharField(max_length=10, blank=False, null=False)
    bookid = models.CharField(max_length=5, blank=False, null=False)
    t_type = models.CharField(max_length=10, blank=False, null=False)
    copies = models.IntegerField(blank=False, null=False)

class Payment_View(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    stud_id = models.CharField(max_length=10, blank=False, null=False)
    bookid = models.CharField(max_length=5, blank=False, null=False)
    amount = models.DecimalField(max_digits=5, decimal_places=2, blank=False, null=False)
    transaction_status = models.CharField(max_length=50, blank=False, null=False)
    transaction_id = models.CharField(max_length=50, blank=False, null=False)

class Books(models.Model):
    bookid = models.CharField(max_length=5, blank=False, null=False)
    bookname = models.CharField(max_length=100, blank=False, null=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    edition = models.IntegerField(blank=False, null=False)
    copies = models.IntegerField(blank=False, null=False)
    shelf = models.IntegerField(blank=False, null=False)
    dept = models.CharField(max_length=50, blank=False, null=False)
