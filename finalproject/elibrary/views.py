from django.shortcuts import render

# Create your views here.

def indexview(request, *args, **kwargs):
    return render(request, 'index.html', {})