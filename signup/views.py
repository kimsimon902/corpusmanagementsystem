from django.db import reset_queries
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import registerUser
from .models import publications
from .models import logoutUser
from django.db.models import Q
from datetime import datetime

# Create your views here.

def home(request):
    results = publications.objects.all()
    return render(request, 'main/home.html',{'publications':results})

def registerView(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name'):
            saverecord = registerUser()
            saverecord.username = request.POST.get('username')
            saverecord.email = request.POST.get('email')
            saverecord.password = request.POST.get('password')
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.save()
            messages.success(request, "Your Account Was Successfully Created")
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            return redirect('/login')#render(request, 'registration/login.html')
    else:
            return render(request, 'registration/register.html')


def loginView(request):
    if request.method=='POST':
        try:
            Userdetails=registerUser.objects.get(email=request.POST['email'],password=request.POST['password'])
            print("Username=",Userdetails)
            request.session['email']=Userdetails.email
            return render(request,'main/home.html')
        except registerUser.DoesNotExist as e:
            messages.success(request,'Username or Password Invalid.')
    return render(request,'registration/login.html')

def logoutView(request):
    try:
        #Userdetails=registerUser.objects.get(email=request.POST['email'])
        saverecord = logoutUser.objects.get(id=5)
        saverecord.username = "tester"
        saverecord.save(['username'])
        del request.session['email']
    except:
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


def PublicationPage(request, id):
    results = publications.objects.filter(id__icontains = id)
    return render(request, 'publication.html',{'publication':results})