from django.urls import path
from . import views


urlpatterns =[
    path('',views.home, name='home'),
    path('register/',views.registerView, name='register'),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('search/',views.searchTest, name ='search'),
    path('publication/<id>/',views.PublicationPage, name ='publicationpage')
]