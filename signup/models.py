from django.db import models, connections
from django.db.models.fields import EmailField
from datetime import date

# Create your models here.

class registerUser(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    last_login = models.CharField(max_length=100)

    class Meta:
        db_table = "auth_user"


class publications(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=200)
    abstract = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='literature/pdfs/')
    class Meta:
        db_table = "publications"
