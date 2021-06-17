from django.shortcuts import render

# Create your views here.


def homepageview(request, *args, **kwargs):
    return render(request, 'librarian/homepage.html', {})


def studentprofileview(request, *args, **kwargs):
    return render(request, 'librarian/studentprofile.html', {})
