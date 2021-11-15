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
    source = models.CharField(max_length=100)
    class Meta:
        db_table = "publications"

class tags(models.Model):
    tagname = models.CharField(max_length=100)

    class Meta:
        db_table = "tags"

class annotations(models.Model):
    author = models.CharField(max_length=100)
    publicationID = models.IntegerField()
    body = models.CharField(max_length=1000)

    class Meta:
        db_table = "annotations"

class bookmarks(models.Model):
    user = models.CharField(max_length=100)
    publicationID = models.CharField(max_length=100)

    class Meta:
        db_table = "bookmarks"

class pubtags(models.Model):
    publication_id = models.CharField(max_length=100)
    tag_id = models.CharField(max_length=100)

    class Meta:
        db_table = "publication_tags"