from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.

def home(request):
   return render(request, 'registration/home.html')

def registerView(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'registration/register.html',{'form':form})


