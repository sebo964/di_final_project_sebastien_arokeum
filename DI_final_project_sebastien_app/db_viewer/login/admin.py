from django.contrib import admin
from login.models import DatabaseConnection, IPData
# Register your models here.

admin.site.register(DatabaseConnection)
admin.site.register(IPData)
