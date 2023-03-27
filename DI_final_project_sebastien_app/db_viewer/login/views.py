from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required


# Create your views here.

def error(request):
    return render(request, 'error.html')      
    
@login_required    
def adminuser(request):
    print("admin user")
    return render(request, 'adminuser.html')

@login_required
def normaluser(request):
    return render(request, 'normaluser.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # adminuser(request, user)
            return render(request, 'adminuser.html')
        else:
             return render(request, 'error.html')
    else:
       return render(request, 'login.html')
        

