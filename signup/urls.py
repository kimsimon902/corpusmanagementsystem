from django import urls
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import signup



urlpatterns =[
    path('',views.home, name='home'),
    path('register/',views.registerView, name='register'),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('search/',views.searchPublication, name ='search'),
    path('publication/<title>/',views.PublicationPage, name ='publicationpage'),
    path('upload/',views.uploadLiterature, name ='upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
