from django.contrib import admin
from django.urls import path , include
from . import views
from login.views import main_logout_user

urlpatterns = [
    path(' ', views.table_details, name="table_details"),
    path('logout', main_logout_user, name="logout"),
    path('table_details/export_to_excel', views.export_table_to_excel, name="table_details_export_excel"),
    path('table_details/export_to_csv', views.export_table_to_csv, name="table_details_export_csv"),
    
    
 
]
