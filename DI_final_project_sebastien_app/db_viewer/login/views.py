from django.shortcuts import render, redirect, get_list_or_404
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
import psycopg2
from django.contrib import messages
from .forms import DatabaseConnectionForm, DatabaseConnectionDeleteForm
from .models import DatabaseConnection

# Create your views here.

def error(request):
    return render(request, 'error.html')      
    
@login_required
def adminsuser(request):
    # Get all database connections
    connections = DatabaseConnection.objects.all()

    # Handle form submission for creating a new connection
    if request.method == 'POST' and 'create-connection' in request.POST:
        form = DatabaseConnectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New database connection created successfully!')
            return redirect('database_connections')
    else:
        form = DatabaseConnectionForm()

    # Handle form submission for deleting a connection
    if request.method == 'POST' and 'delete-connection' in request.POST:
        delete_form = DatabaseConnectionDeleteForm(request.POST)
        if delete_form.is_valid():
            connection_id = request.POST.get('connection_id')
            connection = get_object_or_404(DatabaseConnection, id=connection_id)
            connection.delete()
            messages.success(request, 'Database connection deleted successfully!')
            return redirect('database_connections')
    else:
        delete_form = DatabaseConnectionDeleteForm()

    # Render the template with all database connections and forms
    context = {
        'connections': connections,
        'form': form,
        'delete_form': delete_form,
    }
    
    return render(request, 'adminuser.html', context)

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
        

# -----------------------


@login_required
def database_tables(request):
    # Handle form submission for selecting a database and schema
    if request.method == 'POST':
        database = request.POST.get('database')
        schema = request.POST.get('schema')
        # Create a database connection
        connection = DatabaseConnection.objects.get(name=database).connect()
        cursor = connection.cursor()
        # Get all tables in the selected schema
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = %s", (schema,))
        tables = [table[0] for table in cursor.fetchall()]
        # Render the template with the list of tables
        context = {
            'database': database,
            'schema': schema,
            'tables': tables,
        }
        return render(request, 'database_tables.html', context)

    # Handle form submission for selecting a table and viewing data
    if request.method == 'POST':
        database = request.POST.get('database')
        table = request.POST.get('table')
        # Create a database connection
        connection = DatabaseConnection.objects.get(name=database).connect()
        cursor = connection.cursor()
        # Get the first 500 rows from the selected table
        cursor.execute("SELECT * FROM {} LIMIT 500".format(table))
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        # Render the template with the table data
        context = {
            'database': database,
            'table': table,
            'columns': columns,
            'rows': rows,
        }
        return render(request, 'database_table_data.html', context)

    # Render the template with the database selection form
    connections = DatabaseConnection.objects.all()
    context = {
        'connections': connections,
    }
    return render(request, 'database_selection.html', context)
