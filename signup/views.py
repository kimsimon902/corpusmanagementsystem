from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Userreg
from .models import testData

# Create your views here.

def home(request):
   return render(request, 'registration/home.html')

def registerView(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name'):
            saverecord = Userreg()
            saverecord.username = request.POST.get('username')
            saverecord.email = request.POST.get('email')
            saverecord.password = request.POST.get('password')
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.save()
            messages.success(request, "Your Account Was Successfully Created")
            return render(request, 'registration/register.html')
    else:
            return render(request, 'registration/register.html')


def loginView(request):
    if request.method=='POST':
        try:
            Userdetails=Userreg.objects.get(email=request.POST['email'],password=request.POST['password'])
            print("Username=",Userdetails)
            request.session['email']=Userdetails.email
            return render(request,'registration/home.html')
        except Userreg.DoesNotExist as e:
            messages.success(request,'Username or Password Invalid.')
    return render(request,'registration/login.html')

def logoutView(request):
    try:
        del request.session['email']
    except:
        return render(request,'registration/home.html')
    return render(request,'registration/home.html')
    # if request.method == "POST":
    #     form = UserRegisterForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         messages.success(request, f'Hi {username}, your account was created successfully')
    #         return redirect('home')
    # else:
    #     form = UserRegisterForm()

    # return render(request, 'registration/register.html',{'form':form})

def showTest(request):
    results = testData.objects.all()
    return render(request, 'test/test.html',{'testData':results})

def searchTest(request):
    if request.method == "POST":
        searched = request.POST['searched']
        results = testData.objects.filter(title__icontains=searched)
        return render(request, 'test/search.html',{'searched':searched, 'results':results})
    else:
        return render(request, 'test/search.html',{})