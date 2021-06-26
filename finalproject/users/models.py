from django.db import models
from .helper import duedate
import datetime

# Create your models here.


class Library_Users(models.Model):
    userid = models.CharField(max_length=10, blank=False, null=False)
    password = models.CharField(max_length=15, blank=False, null=False)
    isLibrarian = models.BooleanField(blank=False, null=False)

    def __str__(self):
        return self.userid


class Books(models.Model):
    bookid = models.CharField(max_length=5, blank=False, null=False)
    bookname = models.CharField(max_length=100, blank=False, null=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    edition = models.IntegerField(blank=True, null=True)
    copies = models.IntegerField(blank=False, null=False)
    shelf = models.IntegerField(blank=False, null=False)
    dept = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.bookid


class Issued_Books(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    studid = models.ForeignKey(
        Library_Users, related_name='issue_student_id', on_delete=models.CASCADE)
    libid = models.ForeignKey(
        Library_Users, related_name='issue_librarian_id', on_delete=models.CASCADE)
    bookid = models.ForeignKey(
        Books, related_name='issue_bookid', on_delete=models.CASCADE)
    bookname = models.CharField(
        max_length=100, blank=False, null=False, default="empty")
    duedate = models.DateField(auto_now=False, auto_now_add=False)
    amountdue = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=False, null=False)


class Submitted_Books(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    studid = models.ForeignKey(
        Library_Users, related_name='submit_student_id', on_delete=models.CASCADE)
    libid = models.ForeignKey(
        Library_Users, related_name='submit_librarian_id', on_delete=models.CASCADE)
    bookid = models.ForeignKey(
        Books, related_name='submit_bookid', on_delete=models.CASCADE)
    bookname = models.CharField(
        max_length=100, blank=False, null=False, default="empty")
    amountpaid = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=False, null=False)


class History(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    studid = models.ForeignKey(
        Library_Users, related_name='history_student_id', on_delete=models.CASCADE)
    libid = models.ForeignKey(
        Library_Users, related_name='history_librarian_id', on_delete=models.CASCADE)
    bookid = models.ForeignKey(
        Books, related_name='history_bookid', on_delete=models.CASCADE)
    bookname = models.CharField(
        max_length=100, blank=False, null=False, default="empty")
    ttype = models.CharField(max_length=10, blank=False, null=False)
    copies = models.IntegerField(blank=False, null=False)
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, default=0, blank=False, null=False)


class Payment_View(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    studid = models.ForeignKey(
        Library_Users, related_name='payment_student_id', on_delete=models.CASCADE)
    bookid = models.ForeignKey(
        Books, related_name='payment_bookid', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False)
    transactionid = models.CharField(max_length=50, blank=False, null=False)


class Payment_History(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=False)
    studid = models.ForeignKey(
        Library_Users, related_name='paymenthistory_student_id', on_delete=models.CASCADE)
    bookid = models.ForeignKey(
        Books, related_name='paymenthistory_bookid', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=5, decimal_places=2, blank=False, null=False)
    transactionstatus = models.CharField(
        max_length=50, blank=False, null=False)
    transactionid = models.CharField(max_length=50, blank=False, null=False)
