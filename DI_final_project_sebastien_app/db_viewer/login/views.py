from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import psycopg2
from django.contrib import messages
from .forms import DatabaseConnectionForm
from .models import DatabaseConnection

# Create your views here.

# Login APP  

    # login the user and redirect to the adminuser page if the user is an admin and to the normaluser page if the user is a normal user
    # user the default user profiles in django
    # create two user groups in the django admin page - superadmin and normal user

def main_login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='superadmins').exists():
                return redirect('db_management')
            else:
                return redirect('db_details')
        else:
            messages.error(request, 'Username or Password is incorrect')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
def main_logout_user(request):
    logout(request)
    return redirect('login')
    

