from django import forms
from .models import DatabaseConnection

# Form to create a new database connection
class DatabaseConnectionForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = ['name', 'host', 'port', 'database', 'username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

# Form to delete a database connection
class DatabaseConnectionDeleteForm(forms.ModelForm):
    class Meta:
        model = DatabaseConnection
        fields = []
