from django.shortcuts import render

# Create your views here.


def loginview(request, *args, **kwargs):
    return render(request, 'users/login.html', {})


def setpasswordview(request, *args, **kwargs):
    return render(request, 'users/setpassword.html', {})


def forgotpasswordview(request, *args, **kwargs):
    return render(request, 'users/forgotpassword.html', {})


def viewprofileview(request, *args, **kwargs):
    return render(request, 'users/viewprofile.html', {})


def searchresultview(request, *args, **kwargs):
    return render(request, 'users/searchresult.html', {})
