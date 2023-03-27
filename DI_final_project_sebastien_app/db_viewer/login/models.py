from django.db import models
from django.db import connections

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

    def connect(self):
        # Create connection string
        conn_string = "host='{}' port='{}' dbname='{}' user='{}' password='{}'".format(
            self.host, self.port, self.database, self.username, self.password
        )
        # Use Django's connection handler to create a connection
        connection = connections['default']
        connection.connect()
        connection.cursor()
        connection.connection_string = conn_string
        return connection
