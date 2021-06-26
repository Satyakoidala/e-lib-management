from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

# Create your views here.
from users.forms import *
from .forms import *

from users.models import *
from student.models import *
from .models import *

import datetime

from users.helper import *
from .mailer import *


def homepageview(request, *args, **kwargs):
    username = request.session['curr_user_id']
    searchform = searchboxform()
    studentprofileform = studentsearchform()
    bookform = bookactionform()
    dashboard = Dashboard.objects.get(id=1)
    transactions = History.objects.all().order_by('-id')[:10]

    if 'issue_book_error' in request.session:
        issue_error = request.session['issue_book_error']
        del request.session['issue_book_error']
    else:
        issue_error = ''

    if 'submit_book_error' in request.session:
        submit_error = request.session['submit_book_error']
        del request.session['submit_book_error']
    else:
        submit_error = ''

    if 'mail_notification' in request.session:
        mail_notification = request.session['mail_notification']
        del request.session['mail_notification']
    else:
        mail_notification = ''

    return render(request, 'librarian/homepage.html', {
        'username': username,
        'searchform': searchform,
        'studentprofileform': studentprofileform,
        'bookactionform': bookform,
        'dashboard': dashboard,
        'transactions': transactions,
        'issue_error': issue_error,
        'submit_error': submit_error,
        'mail_notification': mail_notification,
    })


def studentprofileview(request, *args, **kwargs):
    username = request.session['curr_user_id']
    searchform = searchboxform()
    studentprofileform = studentsearchform()
    bookform = bookactionform()
    dashboard = Dashboard.objects.get(id=1)
    transactions = History.objects.all().order_by('-id')[:10]
    errormsg = ''

    if 'issue_book_error' in request.session:
        issue_error = request.session['issue_book_error']
        request.session['issue_book_error'] = ''
    else:
        issue_error = ''

    if 'submit_book_error' in request.session:
        submit_error = request.session['submit_book_error']
        request.session['submit_book_error'] = ''
    else:
        submit_error = ''

    if request.method == 'GET':
        searchedQuery = True
        if request.GET == {}:
            searchedQuery = False
            return HttpResponseRedirect(reverse('librarian:home-page-view'))
        else:
            studentprofileform = studentsearchform(request.GET)
            if studentprofileform.is_valid():
                searchid = studentprofileform.cleaned_data['searchprofile']
                try:
                    user = Library_Users.objects.get(userid=searchid)
                    studentprofile = Students.objects.get(studid=user)
                except:
                    searchedQuery = False
                    return HttpResponseRedirect(reverse('librarian:home-page-view'))

                activebooks = Issued_Books.objects.filter(studid=user)
                for activebook in activebooks:
                    activebook.amountdue = fine(
                        activebook.duedate, datetime.now().date())
                    activebook.save()

                studimage = f'users/images/{studentprofile.studid}.jpg'

                # student id is verified and profile is retrieved!!
                return render(request, 'librarian/studentprofile.html', {
                    'username': username,
                    'searchform': searchform,
                    'studentprofileform': studentprofileform,
                    'searchedquery': searchedQuery,
                    'activebooks': activebooks,
                    'student': studentprofile,
                    'studimage': studimage,
                    'bookactionform': bookform,
                    'dashboard': dashboard,
                    'transactions': transactions,
                    'issue_error': issue_error,
                    'submit_error': submit_error,
                })
            else:
                searchedQuery = False
                return HttpResponseRedirect(reverse('librarian:home-page-view'))

    return render(request, 'librarian/studentprofile.html', {
        'username': username,
        'searchform': searchform,
        'studentprofileform': studentprofileform,
        'searchedquery': False,
        'errors': errormsg,
        'bookactionform': bookform,
        'dashboard': dashboard,
        'transactions': transactions,
        'issue_error': issue_error,
        'submit_error': submit_error,
    })


def issuebookview(request, *args, **kwargs):
    request.session['issue_book_error'] = ''
    if request.method == 'POST':
        worker = Library_Users.objects.get(
            userid=request.session['curr_user_id'])
        active_librarian = Librarian.objects.get(libid=worker)
        bookform = bookactionform(request.POST)
        if bookform.is_valid():
            studid = bookform.cleaned_data['rollno']
            bookid = bookform.cleaned_data['bookid']
            try:
                book = Books.objects.get(bookid=bookid)
            except:
                request.session['issue_book_error'] = 'Invalid Book ID'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))
            try:
                student = Library_Users.objects.get(userid=studid)
            except:
                request.session['issue_book_error'] = 'Invalid Student ID'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))
            # post validity of roll no of student

            activebooks = Issued_Books.objects.filter(studid=student)

            if len(activebooks) == 3:
                request.session['issue_book_error'] = 'Maximum Books Limit Reached'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))

            bookhad = Issued_Books.objects.filter(studid=student, bookid=book)

            if bookhad:
                request.session['issue_book_error'] = 'Book is already taken by this User'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))

            if book.copies <= 0:
                request.session['issue_book_error'] = 'No copies availble for this Book ID'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))

            book.copies -= 1
            book.save()
            timestamp = datetime.now()
            due = duedate(timestamp.date())
            record = Issued_Books(timestamp=timestamp, studid=student,
                                  libid=worker, bookid=book, bookname=book.bookname, duedate=due)
            record.save()
            record = History(timestamp=timestamp, studid=student, libid=worker, bookid=book,
                             bookname=book.bookname, ttype='Issue', copies=book.copies, amount=0)
            record.save()
            dashboard = Dashboard.objects.get(id=1)
            dashboard.booksinside -= 1
            dashboard.issuedbooks += 1
            dashboard.save()
            active_librarian.issuedcount += 1
            active_librarian.totalactions += 1
            active_librarian.save()
        else:
            request.session['issue_book_error'] = 'Invalid details'
    else:
        request.session['issue_book_error'] = 'Invalid action'
    return HttpResponseRedirect(reverse('librarian:home-page-view'))


def submitbookview(request, *args, **kwargs):
    request.session['submit_book_error'] = ''
    if request.method == 'POST':
        worker = Library_Users.objects.get(
            userid=request.session['curr_user_id'])
        active_librarian = Librarian.objects.get(libid=worker)
        bookform = bookactionform(request.POST)
        if bookform.is_valid():
            studid = bookform.cleaned_data['rollno']
            bookid = bookform.cleaned_data['bookid']
            try:
                book = Books.objects.get(bookid=bookid)
            except:
                request.session['submit_book_error'] = 'Invalid Book ID'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))
            try:
                student = Library_Users.objects.get(userid=studid)
            except:
                request.session['submit_book_error'] = 'Invalid Student ID'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))
            # post validity of roll no of student

            # activebooks = Issued_Books.objects.filter(studid=student)

            bookhad = Issued_Books.objects.filter(studid=student, bookid=book)

            if bookhad:
                booktaken = Issued_Books.objects.get(
                    studid=student, bookid=book)
            else:
                request.session['submit_book_error'] = 'Book is not taken by this User'
                return HttpResponseRedirect(reverse('librarian:home-page-view'))

            finepayable = fine(booktaken.duedate, datetime.now().date())
            if booktaken.amountdue == finepayable:
                if finepayable > 0:
                    request.session['submit_book_error'] = f'Book has {finepayable} Rs. of fine to pay!'
                    return HttpResponseRedirect(reverse('librarian:home-page-view'))
                else:
                    pass
            else:
                if finepayable > 0:
                    booktaken.amountdue = finepayable
                    booktaken.save()
                    request.session['submit_book_error'] = f'Book has {finepayable} Rs. of fine to pay!'
                    return HttpResponseRedirect(reverse('librarian:home-page-view'))

            paymentlist = Payment_View.objects.filter(
                studid=student, bookid=book)

            totalpaidamount = 0
            for payment in paymentlist:
                totalpaidamount += payment.amount

            paymentlist.delete()

            book.copies += 1
            book.save()
            timestamp = datetime.now()
            record = Submitted_Books(timestamp=timestamp, studid=student, libid=worker,
                                     bookid=book, bookname=book.bookname, amountpaid=totalpaidamount)
            record.save()
            record = History(timestamp=timestamp, studid=student, libid=worker, bookid=book,
                             bookname=book.bookname, ttype='Submit', copies=book.copies, amount=totalpaidamount)
            record.save()
            booktaken.delete()
            dashboard = Dashboard.objects.get(id=1)
            dashboard.booksinside += 1
            dashboard.submittedbooks += 1
            dashboard.save()
            active_librarian.retrievedcount += 1
            active_librarian.totalactions += 1
            active_librarian.save()
        else:
            request.session['submit_book_error'] = 'Invalid details'
    else:
        request.session['submit_book_error'] = 'Invalid action'
    return HttpResponseRedirect(reverse('librarian:home-page-view'))

def sendnotificationsview(request, *args, **kwargs):
    activebooks = Issued_Books.objects.all()
    date = datetime.now().date()
    for book in activebooks:
        if (book.duedate >= date):
            if diff(date, book.duedate) < 3:
                learner = Library_Users.objects.get(userid=book.studid)
                active_learner = Students.objects.get(studid=learner)
                mailTemplateOne(active_learner, book)
        else:
            book.amountdue = fine(book.duedate, date)
            book.save()
            learner = Library_Users.objects.get(userid=book.studid)
            active_learner = Students.objects.get(studid=learner)
            mailTemplateTwo(active_learner, book)
    request.session['mail_notification'] = 'Notifications sent successfully.'
    return HttpResponseRedirect(reverse('librarian:home-page-view'))
