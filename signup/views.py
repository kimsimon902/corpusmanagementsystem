from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def home(request):
    form = UserCreationForm()
    context = {'form'}
    return render(request, 'signup/register.html', context)
#    return HttpResponse("Testing website")

def registerView(request):
    form = UserCreationForm()
    context = {'form'}
    return render(request, 'registration/register.html', context)


