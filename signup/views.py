from django.db import reset_queries
from django.db.models.fields import EmailField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import registerUser
from .models import publications
from .models import tags
from django.db.models import Q
import time

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def home(request):
    results = publications.objects.all()
    return render(request, 'main/home.html',{'publications':results})

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
    return render(request, 'publication.html',{'publication':results})

def uploadLiterature(request):
    if request.method=='POST':
        if request.POST.get('title') and request.POST.get('author') and request.POST.get('url'):
            savepub = publications()
            savetag = tags()
            savepub.title = request.POST.get('title')
            savepub.author = request.POST.get('author')
            savepub.url = request.POST.get('url')
            savepub.source = request.POST.get('source')
            savepub.pdf = request.FILES.get('document')
            savepub.save()
            for x in range (1,2):
                try:
                    savetag = tags.objects.get(tagname=request.POST.get('textbox' , x))
                except tags.DoesNotExist:
                    savetag.tagname = request.POST.get('textbox' + x)
                    savetag.save()
            return redirect('/')#render(request, 'registration/login.html')
    else:
            return render(request, 'upload.html')