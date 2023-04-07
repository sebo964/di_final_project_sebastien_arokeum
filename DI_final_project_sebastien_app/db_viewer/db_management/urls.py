from django.contrib import admin
from django.urls import path , include
from . import views
from login.views import main_logout_user

urlpatterns = [
    path('db_management', views.database_connection_list, name="db_management"),
    path('logout', main_logout_user, name="logout"),
    path('db_management/add', views.add_database_connection, name="db_management_add"),
    path('db_management/delete', views.delete_database_connection, name="db_management_delete"),
    path('db_management/validate', views.db_connection_validation, name="db_management_validate"),
 
]
