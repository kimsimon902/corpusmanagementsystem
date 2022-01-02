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
    is_superuser = models.CharField(max_length=100)

    class Meta:
        db_table = "auth_user"


class publications(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    abstract = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='literature/pdfs/')
    source = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    year = models.IntegerField()
    
    class Meta:
        db_table = "publications"

class keywords(models.Model):
    keywordname = models.CharField(max_length=100)

    class Meta:
        db_table = "keywords"

class annotations(models.Model):
    author = models.CharField(max_length=100)
    publicationID = models.IntegerField()
    body = models.CharField(max_length=1000)
    folderID = models.IntegerField()
    dateTime = models.CharField(max_length=50)
    marker = models.CharField(max_length=45)
    isEdited = models.IntegerField()

    class Meta:
        db_table = "annotations"

class bookmarks(models.Model):
    user = models.CharField(max_length=100)
    publicationID = models.IntegerField()
    folderID = models.IntegerField()

    class Meta:
        db_table = "bookmarks"

class bookmarks_folder(models.Model):
    folder_name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    class Meta:
        db_table = "bookmarks_folder"

class collaborators(models.Model):
    owner = models.CharField(max_length=100)
    collab = models.CharField(max_length=100)
    folderID = models.IntegerField(max_length=100)

    class Meta:
        db_table = "collaborators"

class pubkeys(models.Model):
    publication_id = models.CharField(max_length=100)
    keywords_id = models.CharField(max_length=100)
    status = models.CharField(max_length=100)

    class Meta:
        db_table = "publication_keywords"

class records_search(models.Model):
    user = models.CharField(max_length=100)
    keyword = models.CharField(max_length=100)
    filter = models.CharField(max_length=45)
    source = models.CharField(max_length=45)
    num_results = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = "records_search"

class records_view_publication(models.Model):
    user = models.CharField(max_length=100)
    pub_title = models.CharField(max_length=500)
    pub_id = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = "records_view_publication"

class records_view_tag(models.Model):
    user = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    date = models.DateField()

    class Meta:
        db_table = "records_view_tag"

class records_bookmark(models.Model):
    user = models.CharField(max_length=100)
    pub_id = models.IntegerField()
    pub_title = models.CharField(max_length=500)
    folder_id = models.IntegerField()
    date = models.DateField()

    class Meta:
        db_table = "records_bookmark"