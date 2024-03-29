from django import urls
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
import signup



urlpatterns =[
    path('',views.index, name='index'),
    path('home/',views.home, name='home'),
    path('about/',views.aboutPage, name='about'),
    path('register/',views.registerView, name='register'),
    path('login/',views.loginView, name='login'),
    path('logout/',views.logoutView, name='logout'),
    path('search/<search>/<filter>',views.filterSearch, name ='filtersearch'),
    path('search/',views.searchPublication, name ='search'),
    path('searchKeywordAnalytics/',views.searchKeywordAnalytics, name ='searchKeywordAnalytics'),
    path('searchAuthorAnalytics/',views.searchAuthorAnalytics, name ='searchAuthorAnalytics'),
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
    path('adminpage/upload-extracts',views.uploadExtracts, name ='pushExcel'),
    path('folder_table/',views.downloadFolderTable, name ='folder_table'),
    path('analytics/<keyword>', views.analytics, name="analytics"),
    path('analytics/<keyword>/<keyword2>', views.analyticsFilterKeyword, name="analyticsFilterKeyword"),
    path('analyticsAuthor/<author>', views.authorAnalytics, name="authorAnalytics"),
    path('analyticsAuthor/<author>/<keyword>', views.authorAnalyticsFilterKeyword, name="authorAnalyticsFilterKeyword"),
    path('testFolderAnalytics/<folderID>', views.FoldersPageAnalytics, name="FoldersPageAnalytics"),
    path('sharedFolderAnalytics/<folderID>/<owner>', views.SharedFoldersPageAnalytics, name="SharedFoldersPageAnalytics"),
    path('centerReports/<yearFilter>', views.centerReports, name="centerReports"),
    path('centerReports/<yearFilter>/<center>', views.centerReportsCenter, name="centerReportsCenter"),
    path('folders/<username>/search/', views.SearchAnnotationFolder, name="searchFolder"),
    path('profile/<user>', views.userProfile, name="userProfile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
