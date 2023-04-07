from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.main_login_user, name="login"),
    path('logout', views.main_logout_user, name="logout"),
 
]
