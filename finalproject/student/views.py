from django.shortcuts import render

# Create your views here.


def homepageview(request, *args, **kwargs):
    return render(request, 'student/homepage.html', {})
