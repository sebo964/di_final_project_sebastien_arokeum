from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import psycopg2
from django.contrib import messages
from login.forms import DatabaseConnectionForm
from login.models import DatabaseConnection
from db_details.views import user_db_select_and_connection
import pandas as pd

# Create your views here.
# table_details APP
    
    # get the table selected by the user from a user input
    
    # from the table put it in a dataframe and show the first 500 rows
    
    # add a option for users to export the data to csv or excel file

@login_required
def table_details(request):
    if request == 'POST':
        database_name = request.POST.get('db_chosen')
        schema_name = request.POST.get('schema_chosen')
        table_name = request.POST.get('table_chosen')
    db_connection = user_db_select_and_connection(database_name)
    conn_db = db_connection.cursor()
    df = pd.DataFrame(conn_db.execute(f"SELECT * FROM {schema_name}.{table_name}").fetchall())
    first_500_rows = df.head(500)
    first_500_rows = first_500_rows.to_html(index=False)
    return render(request, 'table_details.html', {'first_500_rows': first_500_rows})

def export_table_to_csv(request, database_name, schema_name, table_name):
    db_connection = user_db_select_and_connection(database_name)
    conn_db = db_connection.cursor()
    df = pd.DataFrame(conn_db.execute(f"SELECT * FROM {schema_name}.{table_name}").fetchall())
    df.to_csv(f'{table_name}.csv')
    return HttpResponse(f'{table_name}.csv')

def export_table_to_excel(request, database_name, schema_name, table_name):
    db_connection = user_db_select_and_connection(database_name)
    conn_db = db_connection.cursor()
    df = pd.DataFrame(conn_db.execute(f"SELECT * FROM {schema_name}.{table_name}").fetchall())
    df.to_excel(f'{table_name}.xlsx')
    return HttpResponse(f'{table_name}.xlsx')


