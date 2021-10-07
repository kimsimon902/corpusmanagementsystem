from django.urls import path
from . import views


urlpatterns =[
    path('home/',views.home, name='home'),
    #path('login/',views.home, name='home'),
    path('register/',views.registerView, name='register_url'),
]