from django import urls
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import signup



urlpatterns =[
    path('',views.index, name='index'),
    path('home/',views.home, name='home'),
    path('register/',views.registerView, name='register'),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('search/',views.searchPublication, name ='search'),
    path('publication/<id>/',views.PublicationPage, name ='publicationpage'),
    path('publication/<id>/annotate',views.PublicationPageAnnotate, name ='publicationpageannotate'),
    path('publication/<id>/bookmark', views.PublicationBookmark, name = 'publicationbookmark'),
    path('upload/',views.uploadLiterature, name ='upload'),
    path('bookmarks/',views.viewBookmarks, name ='bookmarks'),
    path('adminpage/',views.viewAdmin, name ='bookmarks')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
