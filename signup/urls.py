from django.urls import path
from . import views
import signup



urlpatterns =[
    path('',views.home, name='home'),
    path('register/',views.registerView, name='register'),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('search/',views.searchPublication, name ='search'),
    path('publication/<id>/',views.PublicationPage, name ='publicationpage'),
    path('upload/',views.uploadLiterature, name ='upload')
]