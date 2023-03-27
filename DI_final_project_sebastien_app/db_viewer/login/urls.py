from django.contrib import admin
from django.urls import path , include
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('adminuser', views.adminuser, name='adminuser'),
    path('normaluser', views.normaluser, name='normaluser'),
    path('error', views.error, name='error'),
    
]
