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
    path('search/<search>/<filter>',views.filterSearch, name ='filtersearch'),
    path('search/',views.searchPublication, name ='search'),
    path('folders/<username>/',views.FoldersPage, name ='folders'),
    path('profile/<username>/createfolder',views.createFolder, name ='createfolder'),
    path('folders/<username>/<folderid>/publication/<id>/',views.PublicationPageInFolder, name ='folders-publication-page'),
    path('folders/<username>/<folderid>/publication/<id>/annotate',views.PublicationPageAnnotate, name ='publicationpageannotate'),
    path('folders/<username>/<folderid>/publication/<id>/annotate/<annoID>',views.PublicationPageAnnotateEdit, name ='publicationpageannotateedit'),
    path('folders/<username>/<folderid>/publication/<id>/publicationbookmarkinfolder', views.PublicationBookmarkInFolder, name = 'publicationbookmarkinfolder'),
    path('folders/<username>/addcollab',views.addCollab, name ='addcollab'),
    path('folders/<username>/removecollab',views.deleteCollab, name = 'deletecollab'),
    path('folders/<username>/deletefolder',views.deleteFolder, name = 'deletefolder'),
    path('publication/<id>/addkeywordRequest',views.addKeywordRequest, name = 'addkeywordrequest'),
    path('publication/<id>/removekeywordRequest/<keyword>',views.removeKeywordRequest, name = 'removekeywordrequest'),
    path('publication/<id>/',views.PublicationPage, name ='publicationpage'),
    path('publication/<id>/bookmark', views.PublicationBookmark, name = 'publicationbookmark'),
    path('upload/',views.uploadLiterature, name ='upload'),
    path('bookmarks/',views.viewBookmarks, name ='bookmarks'),
    path('adminpage/',views.viewAdmin, name ='adminpage'),
    path('adminpage/keywordrequests',views.keywordRequests, name ='keywordrequests'),
    path('folder_table/',views.downloadFolderTable, name ='folder_table'),
    path('testAnalytics/<keyword>', views.testAnalytics, name="testAnalytics"),
    path('testFolderAnalytics/<folderID>', views.FoldersPageAnalytics, name="FoldersPageAnalytics"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
