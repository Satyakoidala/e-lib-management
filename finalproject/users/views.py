from .sms import *
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse

from itertools import chain

from .forms import *
from users.models import *
from student.models import *
from librarian.models import *
# Create your views here.

def loginview(request, *args, **kwargs):
    form = loginform()
    try:
        errors = request.session['auth_errors']
        del request.session['auth_errors']
    except:
        errors = ""
    try:
        logoutmsg = request.session['logout_msg']
    except:
        logoutmsg = ''
    if 'logout_msg' in request.session:
        del request.session['logout_msg']
    if 'curr_user_id' in request.session:
        del request.session['curr_user_id']
    if 'issue_book_error' in request.session:
        del request.session['issue_book_error']
    if 'submit_book_error' in request.session:
        del request.session['submit_book_error']
    if 'errors' in request.session:
        del request.session['errors']
    if 'otp_sent' in request.session:
        del request.session['otp_sent']
    if 'otp_session_data' in request.session:
        del request.session['otp_session_data']
    if 'otp_status' in request.session:
        del request.session['otp_status']
    if 'resend_otp' in request.session:
        del request.session['resend_otp']
    return render(request, 'users/login.html', {
        'form': form,
        'errors': errors,
        'logout_msg': logoutmsg,
    })

def validationview(request, *args, **kwargs):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            try:
                user = Library_Users.objects.get(
                    userid=form.cleaned_data['userid'])
            except:
                request.session['curr_user_id'] = 'anonymous'
                request.session['auth_errors'] = 'Invalid Username/Password'
                return HttpResponseRedirect(reverse('users:login-view'))
            if (user.password == form.cleaned_data['psw']):
                request.session['curr_user_id'] = form.cleaned_data['userid']
                # print(request.session['curr_user_id'])
                if (user.isLibrarian):
                    return HttpResponseRedirect(reverse('librarian:home-page-view'))
                else:
                    return HttpResponseRedirect(reverse('student:home-page-view'))
            else:
                request.session['curr_user_id'] = 'anonymous'
                request.session['auth_errors'] = 'Invalid Username/Password'
    return HttpResponseRedirect(reverse('users:login-view'))


def sendotpview(request, *args, **kwargs):
    # valid incoming user from the request
    # print(request.session['curr_user_id'])
    try:
        user = Library_Users.objects.get(
            userid=request.session['curr_user_id'])
        if user.isLibrarian:
            active_user = Librarian.objects.get(libid=user)
        else:
            active_user = Students.objects.get(studid=user)
        request.session['otp_session_data'] = send_otp(active_user.phone)
        request.session['otp_sent'] = True
    except:
        request.session['curr_user_id'] = 'anonymous'
        request.session['errors'] = 'Invalid User ID'
        request.session['otp_sent'] = False
    
    return HttpResponseRedirect(reverse('users:forgot-password-view'))

def verifyotpview(request, *args, **kwargs):
    request.session['otp_status'] = ''
    if request.method == 'POST':
        verification_form = verifyotpform(request.POST)
        if verification_form.is_valid():
            response_data = otp_verification(request, verification_form.cleaned_data['otp'])
            if response_data['Message'] == 'Success':
                request.session['otp_status'] = 'Success'
                return HttpResponseRedirect(reverse('users:set-password-view'))
            else:
                request.session['otp_status'] = 'Invalid OTP!'
                otpform = sendotpform()
                errors = ''
                verify_otpform = verifyotpform()
                return  render(request, 'users/forgotpassword.html', {
                    'sent_otp': request.session['otp_sent'],
                    'otpform': otpform,
                    'verify_otpform': verify_otpform,
                    'errors': errors,
                    'resend_otp': False,
                    'otp_status': request.session['otp_status'],
                })
        else:
            request.session['otp_status'] = 'Invalid OTP!'
            return HttpResponseRedirect(reverse('users:forgot-password-view'))

def forgotpasswordview(request, *args, **kwargs):
    if request.method == 'POST':
        if request.session['otp_sent']:
            otpform = sendotpform()
            errors = ''
            return render(request, 'users/forgotpassword.html', {
                'sent_otp': request.session['otp_sent'],
                'otpform': otpform,
                'errors': errors,
            })
        else:
            print(request.POST)
            otpform = sendotpform(request.POST)
            if otpform.is_valid():
                request.session['curr_user_id'] = otpform.cleaned_data['userid']
                print(request.session['curr_user_id'])
            else:
                request.session['curr_user_id'] = 'xxx'
            return HttpResponseRedirect(reverse('users:send-otp-view'))
    else:
        try:
            if request.session['otp_sent']:
                otpform = sendotpform()
                errors = ''
                verify_otpform = verifyotpform()
                try:
                    if request.session['resend_otp']:
                        resend_otp = True
                        request.session['resend_otp'] = False
                except:
                    request.session['resend_otp'] = False
                    resend_otp = False

                return render(request, 'users/forgotpassword.html', {
                    'sent_otp': request.session['otp_sent'],
                    'otpform': otpform,
                    'verify_otpform': verify_otpform,
                    'errors': errors,
                    'resend_otp': resend_otp,
                })
            else:
                otpform = sendotpform()
                errors = request.session['errors']
                del request.session['errors']
        except:
            request.session['otp_sent'] = False
            otpform = sendotpform()
            errors = ''
    return render(request, 'users/forgotpassword.html', {
        'sent_otp': request.session['otp_sent'],
        'otpform': otpform,
        'errors': errors,
    })

def resendotpview(request, *args, **kwargs):
    request.session['resend_otp'] = True
    return HttpResponseRedirect(reverse('users:send-otp-view'))

def setpasswordview(request, *args, **kwargs):
    pswform = setpasswordform()
    try:
        errors = request.session['password_errors']
        del request.session['password_errors']
    except:
        errors = ""
    return render(request, 'users/setpassword.html', {
        'pswform': pswform,
        'pswerrors': errors,
    })

def updatepasswordview(request, *args, **kwargs):
    if request.method == 'POST':
        pswform = setpasswordform(request.POST)
        if pswform.is_valid():
            if pswform.cleaned_data['psw1'] == pswform.cleaned_data['psw2']:
                user = Library_Users.objects.get(
                    userid=request.session['curr_user_id'])
                user.password = pswform.cleaned_data['psw1']
                user.save()
                if (user.isLibrarian):
                    return HttpResponseRedirect(reverse('librarian:home-page-view'))
                else:
                    return HttpResponseRedirect(reverse('student:home-page-view'))
            else:
                request.session['password_errors'] = 'New Password not matching with Retyped Password!!'
                return HttpResponseRedirect(reverse('users:set-password-view'))
    else:
        return HttpResponseRedirect(reverse('users:set-password-view'))

def logoutview(request, *args, **kwargs):
    request.session['logout_msg'] =  'You have been logged out successfully!!'
    return HttpResponseRedirect(reverse('users:login-view'))

def viewprofileview(request, *args, **kwargs):
    user = Library_Users.objects.get(userid=request.session['curr_user_id'])
    profileimgurl = f'users/images/{user.userid}.jpg'
    if user.isLibrarian:
        librarian = Librarian.objects.get(libid=user)
        return render(request, 'users/viewprofile.html', {
            'username': user.userid,
            'librarian': librarian,
            'isLibrarian': user.isLibrarian,
            'profileImage': profileimgurl,
        })
    else:
        student = Students.objects.get(studid=user)
        return render(request, 'users/viewprofile.html', {
            'username': user.userid,
            'student': student,
            'isLibrarian': user.isLibrarian,
            'profileImage': profileimgurl,
        })


def searchresultview(request, *args, **kwargs):
    username = request.session['curr_user_id']
    user = Library_Users.objects.get(userid=username)
    if request.method == 'GET':
        searchform = searchboxform(request.GET)
        if searchform.is_valid():
            keyword = searchform.cleaned_data['searchbox']
            keywords = keyword.split()
            if len(keywords) < 2:
                if len(keywords) == 1:
                    booklist = Books.objects.filter(
                        bookname__icontains=keywords[0])
                else:
                    booklist = {}
            else:
                booklist = list()
                for word in keywords:
                    booklist.append(Books.objects.filter(
                        bookname__icontains=word))
                booklist = list(chain(*booklist))
            return render(request, 'users/searchresult.html', {
                'username': username,
                'searchform': searchboxform(),
                'booklist': booklist,
                'user': user,
            })
    return render(request, 'users/searchresult.html', {
        'username': username,
        'searchform': searchboxform(),
        'user': user,
    })
