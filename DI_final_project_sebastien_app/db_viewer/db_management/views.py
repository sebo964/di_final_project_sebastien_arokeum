from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import psycopg2
from django.contrib import messages
from login.models import DatabaseConnection
import pandas as pd
from login.views import main_login_user, main_logout_user
from .forms import DatabaseConnectionForm




def database_connection_list(request):
    if request.user.is_authenticated:
        # check if the user is in the superadmin group
            # get all the database connection objects
            database_connections = DatabaseConnection.objects.all()
            database_connections = database_connections.order_by('name')
            database_connections = database_connections.values()
            form = DatabaseConnectionForm(request.POST)
            return render (request, 'db_management.html', {'database_connections': database_connections, 'form': form})
    else:
            print("no")
            return redirect('login')    
    
# add a new database connection
def add_database_connection(request):
    if request.method == 'POST':
        form = DatabaseConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('db_management') # or any other URL you want to redirect to
    else:
        form = DatabaseConnectionForm()

    context = {'form': form}
    return render(request, 'db_management', context)
        
        
def delete_database_connection(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            dbname = request.POST['database'] # get the id of the database connection to delete']  
            database_connection = DatabaseConnection.objects.get(database=dbname) 
            # delete the database connection object
            database_connection.delete()
            # show message 'database connection deleted' and redirect to the database connection list page
            return messages.success(request, 'Database connection deleted')
        else:
            return redirect('userlogin')
        
        
        
        
def db_connection_validation(request, id):
    if request.user.is_authenticated:        # check if the user is in the superadmin group
        if request.method == 'POST':
            id = int(id)
            database_connection = DatabaseConnection.objects.get(id=id)
            # get the details from the database connection object
            host = database_connection.host
            port = database_connection.port
            database = database_connection.database
            username = database_connection.username
            password = database_connection.password
            # try to connect to the database
            try:
                conn = psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=username,
                    password=password,
                )
                # show message 'database connection valid' and redirect to the database connection list page
                return HttpResponse('Database connection valid')
            except:
                # show message 'database connection invalid' and redirect to the database connection list page
                return HttpResponse('Database connection invalid')
        else:
            return redirect('login')