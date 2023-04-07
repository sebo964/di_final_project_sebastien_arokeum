from django.db import models

# Model to store database connections details
class DatabaseConnection(models.Model):
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    port = models.IntegerField()
    database = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class IPData(models.Model):
    ip_address = models.CharField(max_length=100, unique=True)
    session_start_date = models.DateTimeField(auto_now_add=True)
    organization_info = models.CharField(max_length=100, blank=True)
    country_info = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = "ip_data"