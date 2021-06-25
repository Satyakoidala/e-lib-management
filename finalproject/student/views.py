from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from users.forms import *
from users.models import *
from student.models import *

from users.helper import *

import datetime
import uuid

def homepageview(request, *args, **kwargs):
    username = request.session['curr_user_id']
    active_user = Library_Users.objects.get(userid=username)
    searchform = searchboxform()
    activebooks = Issued_Books.objects.filter(studid=active_user)
    for activebook in activebooks:
        activebook.amountdue = fine(activebook.duedate, datetime.datetime.now().date())
        activebook.save()
    actionhistory = History.objects.filter(studid=active_user).order_by('-id')[:10]
    if 'pay_status' in request.session:
        pay_status = request.session['pay_status']
        del request.session['pay_status']
    else:
        pay_status=''
    return render(request, 'student/homepage.html', {
        'username': username,
        'searchform': searchform,
        'activebooks': activebooks,
        'actionhistory': actionhistory,
        'paystatus': pay_status,
    })


def paymentview(request, bookid, *args, **kwargs):
    username = request.session['curr_user_id']
    active_user = Library_Users.objects.get(userid=username)
    book = Books.objects.get(bookid=bookid)
    paymentbook = Issued_Books.objects.get(studid=active_user, bookid=book)
    if paymentbook.amountdue<=0:
        return HttpResponseRedirect(reverse('student:home-page-view'))
    
    return render(request, 'student/payment.html', {
        'user': active_user,
        'paymentbook': paymentbook,
    })

def paymentsuccessview(request, bookid, *args, **kwargs):
    username = request.session['curr_user_id']
    active_user = Library_Users.objects.get(userid=username)
    student = Students.objects.get(studid=active_user) 
    book = Books.objects.get(bookid=bookid)
    paymentbook = Issued_Books.objects.get(studid=active_user, bookid=book)
    timestamp = datetime.datetime.now()
    transaction_id = uuid.uuid1().hex
    amount_paid = paymentbook.amountdue
    payview = Payment_View(timestamp=timestamp, studid=active_user, bookid=book, amount=amount_paid, transactionid=transaction_id)
    payview.save()
    payhistory = Payment_History(timestamp=timestamp, studid=active_user, bookid=book, amount=amount_paid, transactionstatus='success', transactionid=transaction_id)
    payhistory.save()
    paymentbook.duedate = timestamp.date()
    paymentbook.amountdue = 0
    paymentbook.save()
    student.amountpaid += amount_paid
    student.save()
    request.session['pay_status'] = 'Payment Successful!!'
    return HttpResponseRedirect(reverse('student:home-page-view'))
    

def paymentfailureview(request, bookid, *args, **kwargs):
    username = request.session['curr_user_id']
    active_user = Library_Users.objects.get(userid=username)
    student = Students.objects.get(studid=active_user) 
    book = Books.objects.get(bookid=bookid)
    paymentbook = Issued_Books.objects.get(studid=active_user, bookid=book)
    timestamp = datetime.datetime.now()
    transaction_id = uuid.uuid1().hex
    amount_involved = paymentbook.amountdue
    payhistory = Payment_History(timestamp=timestamp, studid=active_user, bookid=book, amount=amount_involved, transactionstatus='failure', transactionid=transaction_id)
    payhistory.save()
    request.session['pay_status'] = 'Payment Failed!!'
    return HttpResponseRedirect(reverse('student:home-page-view'))