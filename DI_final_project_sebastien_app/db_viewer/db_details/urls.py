from django.contrib import admin
from django.urls import path , include
from . import views
from login.views import main_logout_user

urlpatterns = [
    path('', views.db_list, name="db_details"),
    path('logout', main_logout_user, name="logout"),
    path('schema', views.list_schemas_in_database, name="db_details_schema"),
    path('schematable', views.show_tables_and_headers_in_schema, name="db_details_schema_table"),
]
