from django.db import reset_queries
from django.db.models.fields import EmailField, NullBooleanField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import pubtags, registerUser
from .models import publications
from .models import tags
from .models import annotations
from .models import bookmarks
from .models import pubtags
from django.db.models import Q
import time

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def home(request):
    results = publications.objects.all()
    return render(request, 'main/home.html',{'publications':results})

def viewBookmarks(request):
    user = request.session['username']
  
    bookmark = bookmarks.objects.filter(user=user).values('publicationID')
    publication = publications.objects.filter(id__in=bookmark)

    

    return render(request, 'bookmarks.html', {'publications':publication})

#Creates a user account and stores it in the database
def registerView(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name'):
            saverecord = registerUser()
            saverecord.username = request.POST.get('username')
            if registerUser.objects.filter(username=request.POST.get('username')).exists():
                messages.error(request, 'Sorry. This username is taken', extra_tags='name')
                return redirect('register')
            saverecord.email = request.POST.get('email')
            if registerUser.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'Email already has an account', extra_tags='name')
                return redirect('register')
            saverecord.password = request.POST.get('password')
            if saverecord.password != request.POST.get('repwd'):
                messages.error(request, 'Password does not match', extra_tags='name')
                return redirect('register')
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
            saverecord.save()
            return redirect('login')#render(request, 'registration/login.html')
    else:
            return render(request, 'registration/register.html')

#Checks database if account exists and authenticates the user
def loginView(request):
    if request.method=='POST':
        try:
            Userdetails=registerUser.objects.get(email=request.POST['email'],password=request.POST['password'])
            print("Username=",Userdetails)
            request.session['email']=Userdetails.email
            request.session['username']=Userdetails.username
            return redirect('home')
        except registerUser.DoesNotExist as e:
            messages.error(request,'Username or Password Invalid.', extra_tags='name')
            return redirect('login')
    return render(request,'registration/login.html')

def logoutView(request):
    try:
        auth_user = registerUser.objects.get(email = request.session['email'])
        auth_user.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
        auth_user.save()
        del request.session['email']
    except registerUser.DoesNotExist:
        return redirect('/')
    return redirect('/')

def showTest(request):
    results = publications.objects.all()
    return render(request, 'test/test.html',{'publications':results})

def searchPublication(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searchFilter = request.POST['filterData']

        if  searchFilter == "default":
            results = publications.objects.filter(
                Q(title__icontains=searched) |
                Q(author__icontains=searched) |
                Q(abstract__icontains=searched) |
                Q(url__icontains=searched)
            )
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        elif searchFilter == "title":
            results = publications.objects.filter(title__icontains=searched)
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        elif searchFilter == "author":
            results = publications.objects.filter(author__icontains=searched)
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        elif searchFilter == "abstract":
            results = publications.objects.filter(abstract__icontains=searched)
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        elif searchFilter == "url":
            results = publications.objects.filter(url__icontains=searched)
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        else:
            return render(request, 'main/search.html',{})
        
    else:
        return render(request, 'main/search.html',{})

#this function displays the details of a publication that has been selected from the home page
def PublicationPage(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author= request.session['username']
    else:
        author="null"
    annotation = annotations.objects.filter(publicationID=id, author=author)
    bookmark = bookmarks.objects.filter(publicationID=id, user=author)
    return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'bookmarks':bookmark})

def PublicationPageAnnotate(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author= request.session['username']
    else:
        author="null"
    annotation = annotations.objects.filter(publicationID=id, author=author)
    
    if request.method=='POST':
        body= request.POST['annotation']
        # author="localtest"
        pubID = id
        saveAnnotation = annotations()
        saveAnnotation.author = author
        saveAnnotation.body = body
        saveAnnotation.publicationID = pubID
        saveAnnotation.save()
        return render(request, 'publication.html',{'publication':results, 'annotations':annotation})
    else:
        return render(request, 'publication.html', {'publication':results, 'annotations':annotation})

def PublicationBookmark(request, id):
    results = publications.objects.filter(id=id)

    if(request.user):
        user = request.session['username']
    else:
        user = "null"

    bookmark = bookmarks.objects.filter(publicationID=id, user=user)
    annotation = annotations.objects.filter(publicationID=id, author=user)

    if request.method=='POST':
        if 'bookmark-add' in request.POST:
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = user
            addBookmark.publicationID = pubID
            addBookmark.save()
            return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
        elif 'bookmark-delete' in request.POST:
            bookmark.delete()
            return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
        else:
            return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
    else:
        return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})


def uploadLiterature(request):
    if request.method=='POST':
        if request.POST.get('title') and request.POST.get('author') and request.POST.get('url'):
            savepub = publications()
            savepub.title = request.POST.get('title')
            savepub.author = request.POST.get('author')
            savepub.url = request.POST.get('url')
            savepub.source = request.POST.get('source')
            savepub.pdf = request.FILES.get('document')
            savepub.save()
            insert_list = []
            name_id = []
            insert_id = []
            pub_id = []
            for i in range(1,10):
                if request.POST.get('textbox' + str(i)) is not None:
                    if tags.objects.filter(tagname=request.POST.get('textbox' + str(i))).exists():
                            name_id.append(request.POST.get('textbox' + str(i)))
                    else:
                        insert_list.append(tags(tagname=request.POST.get('textbox' + str(i))))
                        name_id.append(request.POST.get('textbox' + str(i)))
            tags.objects.bulk_create(insert_list)
            results = publications.objects.filter(title = savepub.title)
            for j in range(0,len(name_id)-1):
                store = tags.objects.filter(tagname=name_id[j])
                pub_id.append(pubtags(publication_id=int(results.id)))
                insert_id.append(pubtags(tag_id=int(store.id)))
            pubtags.objects.bulk_create(insert_id, pub_id)
            return redirect('/')#render(request, 'registration/login.html')
    else:
            return render(request, 'upload.html')

# def annotateFromPub(request):
#     results = publications.objects.filter(id=id)
#     if request.method=='POST':
#         body= request.POST['annotation']
#         author= request.session['username']
#         pubID = id
#         saveAnnotation = annotations()
#         saveAnnotation.author = author
#         saveAnnotation.body = body
#         saveAnnotation.publicationID = pubID
#         saveAnnotation.save()
#         return render(request, 'publication.html',{'publication':results})