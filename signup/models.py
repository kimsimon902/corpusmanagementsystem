from django.db import models
from django.db.models.fields import EmailField
from datetime import date

# Create your models here.

class Userreg(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    class Meta:
        db_table = "auth_user"