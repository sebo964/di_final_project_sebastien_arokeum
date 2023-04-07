from django import forms
from login.models import DatabaseConnection

class DatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = ('name', 'host', 'port', 'database', 'username', 'password')