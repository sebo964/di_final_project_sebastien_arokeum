from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import psycopg2
from django.contrib import messages
from login.models import DatabaseConnection

# Create your views here.


# connect to the main database that stores the user database connection details
def main_db_connect():

    db_connection = psycopg2.connect( 
        host='ep-steep-rice-561755.ap-southeast-1.aws.neon.tech',
        port='5432',
        dbname='di_final_project',
        user='sebo964',
        password='cKoai9SPCp0z',
        sslmode='require'
    )
    print ("Main Database connection successful")
    return db_connection

# takes the user database connection details and connects to the user database selected by the user returns the live connection
def connect_user_db(listofdicts):
    try:
        print(f"listofdicts: {listofdicts}, connect user function")
        host = listofdicts['host']
        port = listofdicts['port']
        name = listofdicts['database']
        user= listofdicts['username']
        password = listofdicts['password']
        db_user_connection = psycopg2.connect( 
            host=host,
            port=port,
            dbname=name,
            user=user,
            password=password,
        )
        print ("User Database connection successful")
        return db_user_connection
    except psycopg2.Error as e:
            print("Error connecting to user database:")
            print(f"- Error message: {e}")
            print(f"- Error code: {e.pgcode}")
            print(f"- Error reason: {e.pgerror}")
            return None

@login_required
def db_list(request):
    list_of_database = DatabaseConnection.objects.all()
    return render(request, 'db_details.html', {'list_of_database_names': list_of_database})


# takes the database name selected, connect to the main database and returns the live connection
# then takes the name provided, find the matching database details stored in the main database, returns all the details in a dictionary
# passes the details the connect_user_db function to connect to the user selected database. 
def user_db_select_and_connection(name):
    db_connections = main_db_connect()
    cursor = db_connections.cursor()
    
    cursor.execute(f"SELECT * FROM login_databaseconnection WHERE name = '{name}'")
    # from database connection model in models.py return the entry that matches database name
    
    # listofdicts = DatabaseConnection.objects.get(name=name)

    listofdicts = [dict(zip([key[0] for key in cursor.description], row)) for row in cursor.fetchall()]
    listofdicts_dicts = {}
    for i in listofdicts:
        print(f"this is i: {i}")
        listofdicts_dicts.update(i)
    print(f"listofdicts_dicts: {listofdicts_dicts}")
    db_user_connection = connect_user_db(listofdicts_dicts)
    return db_user_connection

def list_schemas_in_database(request):
    if request.method == 'POST':
        selected_database = request.POST.get('db_chosen')
        print(selected_database)
        db_connection = user_db_select_and_connection(selected_database)
        conn_db = db_connection.cursor()
        list_of_schemas = conn_db.execute("SELECT schema_name FROM information_schema.schemata")
        db_chosen = selected_database
        print(f"list_of_schemas: {list_of_schemas}")
        return render(request, 'db_schema.html', {'list_of_schemas': list_of_schemas, 'db_chosen': db_chosen})
    else:
        return redirect('db_details')

def show_tables_and_headers_in_schema(request, database_name, schema_name):
    db_connection = user_db_select_and_connection(database_name)
    conn_db = db_connection.cursor()
    conn_db.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'")
    list_of_tables = conn_db.fetchall()
    dict_of_tables_and_headers = {}
    for table in list_of_tables:
        conn_db.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema_name}' AND table_name = '{table}'")
        dict_of_tables_and_headers[table] = conn_db.fetchall()    
    return render(request, 'db_tables.html', {'dict_of_tables_and_headers': dict_of_tables_and_headers})

