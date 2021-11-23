from django.core import paginator
from django.db import reset_queries
from django.db.models.fields import EmailField, NullBooleanField
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import pubkeys, registerUser
from .models import publications
from .models import keywords
from .models import annotations
from .models import bookmarks
from .models import bookmarks_folder
from .models import collaborators
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator
import time

# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def home(request):
    results = publications.objects.all()
    annotation = annotations.objects.all()
    return render(request, 'main/home.html',{'publications':results, 'annotations': annotation})

def viewBookmarks(request):
    email = request.session['email']
  
    bookmark = bookmarks.objects.filter(email=email).values('publicationID')
    publication = publications.objects.filter(id__in=bookmark)

    

    return render(request, 'bookmarks.html', {'publications':publication})

#Creates a user account and stores it in the database
def registerView(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name'):
            saverecord = registerUser()
            saverecord.username = request.POST.get('username')
            if registerUser.objects.filter(username=request.POST.get('username')).exists():
                messages.error(request, 'Sorry. This username is taken', extra_tags='name')
                return redirect('register')
            saverecord.email = request.POST.get('email')
            if registerUser.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'Email already has an account', extra_tags='name')
                return redirect('register')
            saverecord.password = request.POST.get('password')
            if saverecord.password != request.POST.get('repwd'):
                messages.error(request, 'Password does not match', extra_tags='name')
                return redirect('register')
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.is_superuser = 0
            saverecord.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
            saverecord.save()
            myupload = bookmarks_folder()
            myupload.folder_name = 'My Uploads'
            myupload.user = request.POST.get('email')
            myupload.save()
            request.session['email']= request.POST.get('email')
            request.session['username']= request.POST.get('username')
            request.session['is_superuser'] = 0
            return redirect('home')#render(request, 'registration/login.html')
    else:
            return render(request, 'registration/register.html')

#Checks database if account exists and authenticates the user
def loginView(request):
    if request.method=='POST':
        try:
            Userdetails=registerUser.objects.get(email=request.POST['email'],password=request.POST['password'])
            if Userdetails.is_superuser == 1:
                request.session['email']=Userdetails.email
                request.session['username']=Userdetails.username
                request.session['is_superuser']=Userdetails.is_superuser
                return redirect('adminpage')
            else:
                request.session['email']=Userdetails.email
                request.session['username']=Userdetails.username
                request.session['is_superuser']=Userdetails.is_superuser
                return redirect('home')
        except registerUser.DoesNotExist as e:
            messages.error(request,'Username or Password Invalid.', extra_tags='name')
            return redirect('login')
    return render(request,'registration/login.html')

def logoutView(request):
    try:
        auth_user = registerUser.objects.get(email = request.session['email'])
        auth_user.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
        auth_user.save()
        del request.session['email']
    except registerUser.DoesNotExist:
        return redirect('/')
    return redirect('/')

def showTest(request):
    results = publications.objects.all()
    annotation = annotations.objects.all()
    return render(request, 'test/test.html',{'publications':results, 'annotations': annotation})

def searchPublication(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searchFilter = request.POST['filterData']
        
        libFilter = request.POST.getlist('filterLib')

        if  searchFilter == "default":

            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains='ais', status__icontains="approved"
            )


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains='ais') |
                    Q(source__icontains='ieee')
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                )        


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                )


            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="ieee", status__icontains="approved"
            )

                
            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
               results = publications.objects.filter(
                    Q(source__icontains="ieee") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                )


            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="scopus", status__icontains="approved"
            )
            else:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
            )

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   

            page_results = Paginator(results, 10)
            page_number = 1
            page_obj = page_results.get_page(page_number)        

            return render(request, 'main/search.html',{'searched':searched, 'results':results })

        elif searchFilter == "title":
            
            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched,source__icontains="ais", status__icontains="approved")


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ais") |
                    Q(source__icontains="ieee"), title__icontains=searched, status__icontains="approved"
                )


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ais") |
                    Q(source__icontains="scopus"), title__icontains=searched, status__icontains="approved"
                )

                
            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched,source__icontains="ieee", status__icontains="approved")


            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ieee") |
                    Q(source__icontains="scopus"), title__icontains=searched, status__icontains="approved"
                )
                
            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched, source__icontains="scopus", status__icontains="approved")


            else:
                results = publications.objects.filter(title__icontains=searched, status__icontains="approved")
 

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   

            return render(request, 'main/search.html',{'searched':searched, 'results':results})

        elif searchFilter == "author":

            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched,source__icontains="ais", status__icontains="approved")


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais")|
                    Q(source__icontains="ieee"), author__icontains=searched, status__icontains="approved"
                )


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais")|
                    Q(source__icontains="scopus"), author__icontains=searched, status__icontains="approved"
                )


            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched,source__icontains="ieee", status__icontains="approved")


            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ieee")|
                    Q(source__icontains="scopus"), author__icontains=searched, status__icontains="approved"
                )

            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched, source__icontains="scopus", status__icontains="approved")    


            else:
                results = publications.objects.filter(author__icontains=searched, status__icontains="approved")

            

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()    

            return render(request, 'main/search.html',{'searched':searched, 'results':results})
    else:
        
        pubs = publications.objects.all()
        xlist =     list(pubs)

        for publication in xlist:
            if publication.url == 'doi.org/' or len(publication.url) == 0:
                publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                publication.save()  

        return render(request, 'main/search.html',{})

def FoldersPage(request, username):

    email = request.session['email']

    rawbookmarks = bookmarks.objects.filter(user=email) #All bookmarks of the user
    filterpub = bookmarks.objects.filter(user=email).values('publicationID') #Get the publicationIDs of bookmarks of the user
    folders = bookmarks_folder.objects.filter(user=email) #Get folders made by the user
    collaborator = collaborators.objects.filter(owner=email) #Get the collaborators

    bookmark = publications.objects.filter(id__in=filterpub) #Get the publications that is bookmarked

    collabs = collaborators.objects.filter(collab=email).values('folderID') #Get the folderIDs of the folders that have collaborators
    shared_folders = bookmarks_folder.objects.filter(id__in=collabs) #The folders that have collaborators

    shared_folders_ids = bookmarks_folder.objects.filter(id__in=collabs).values('id') #Get the ids of the folders that have collaborators
    shared_folders_pubs = bookmark.filter(folderID__in=shared_folders_ids) #Get the publications that are shared
    

    return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedpubs':shared_folders_pubs})

#this function displays the details of a publication that has been selected from the home page
def PublicationPage(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author = request.session['username']
    else:
        author="null"

    email = request.session['email']

    annotation = annotations.objects.filter(publicationID=id, author=author)


    my_folders = bookmarks_folder.objects.filter(user=email)
    folders_value = bookmarks_folder.objects.filter(user=email).values('id')


    bookmark_value = bookmarks.objects.filter(publicationID=id, folderID__in=folders_value).values('folderID')


    in_bookmark = bookmarks_folder.objects.filter(id__in=bookmark_value)
    not_bookmark = bookmarks_folder.objects.exclude(id__in=bookmark_value).filter(id__in=folders_value)


    return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'my_folders':my_folders, 'in_bookmark':in_bookmark, 'not_bookmark':not_bookmark})

def PublicationPageInFolder(request, folderid, username, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author = request.session['username']
    else:
        author="null"

    email = request.session['email']

    annotation = annotations.objects.filter(publicationID=id, folderID=folderid)
    collaborator = collaborators.objects.filter(owner=email)

    my_folders = bookmarks_folder.objects.filter(user=email)
    folders_value = bookmarks_folder.objects.filter(user=email).values('id')

    bookmark_value = bookmarks.objects.filter(publicationID=id, folderID__in=folders_value).values('folderID')

    in_bookmark = bookmarks_folder.objects.filter(id__in=bookmark_value)
    not_bookmark = bookmarks_folder.objects.exclude(id__in=bookmark_value).filter(id__in=folders_value)


    return render(request, 'publication-folder.html', {'publication':results, 'annotations':annotation, 'my_folders':my_folders, 'in_bookmark':in_bookmark, 'not_bookmark':not_bookmark, 'folderID': folderid, 'pubID': id, 'collaborators':collaborator})


def PublicationPageAnnotate(request, username, folderid, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author= request.session['username']
    else:
        author="null"
    
    email = request.session['email']
    annotation = annotations.objects.filter(publicationID=id, author=author)
    collaborator = collaborators.objects.filter(owner=email)
    next = request.POST.get('next', '/')
    current_datetime = datetime.now()
    mark = request.POST['selectMark']
    
    if request.method=='POST':
        if 'annotate-add' in request.POST:
            body= request.POST['annotation']
            pubID = id
            saveAnnotation = annotations()
            saveAnnotation.author = author
            saveAnnotation.body = body
            saveAnnotation.publicationID = pubID
            saveAnnotation.folderID = folderid
            saveAnnotation.dateTime = current_datetime
            saveAnnotation.marker = mark
            saveAnnotation.save()
            messages.success(request, "Annotation saved")
            return HttpResponseRedirect(next)
    else:
        return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'collaborators':collaborator})

def PublicationPageAnnotateEdit(request, username, folderid, id, annoID):
    results = publications.objects.filter(id=id)
    if (request.user):
        author= request.session['username']
    else:
        author="null"

    email = request.session['email']
    annotation = annotations.objects.filter(publicationID=id, author=author, id=annoID)
    collaborator = collaborators.objects.filter(owner=email)
    next = request.POST.get('next', '/')
    current_datetime = datetime.now()
    
    
    if request.method=='POST':
        if 'annotate-save' in request.POST:
            annotation.delete()
            mark = request.POST['selectMark']
            body= request.POST['annotation-exist']
            pubID = id
            saveAnnotation = annotations()
            saveAnnotation.author = author
            saveAnnotation.body = body
            saveAnnotation.publicationID = pubID
            saveAnnotation.folderID = folderid
            saveAnnotation.dateTime = current_datetime
            saveAnnotation.marker = mark
            saveAnnotation.save()
            messages.success(request, "Annotation edited")
            return HttpResponseRedirect(next)
        else:
            annotation.delete()
            messages.success(request, "Annotation deleted")
            return HttpResponseRedirect(next)
    else:
        return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'collaborators':collaborator})

def PublicationBookmark(request, id):
    results = publications.objects.filter(id=id)
    pubID = id
    if(request.user):
        user = request.session['username']
    else:
        user = "null"

    email = request.session['email']
    bookmark = bookmarks.objects.filter(publicationID=id, user=email)
    annotation = annotations.objects.filter(publicationID=id, author=user)
    next = request.POST.get('next', '/')

    if request.method=='POST':
        if request.POST.get("bookmark_action") == 'add':
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = email
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()
            messages.success(request, "Added to your bookmarks")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return HttpResponseRedirect(next)
        elif request.POST.get("bookmark_action") == 'delete':
            folder_value = request.POST.get('folder_id')
            bookmarks.objects.filter(folderID=folder_value, publicationID=pubID, user=email).delete()

            messages.success(request, "Deleted from your bookmarks")
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

        elif request.POST.get("newFolder") == 'newFolder':
            newFolder = bookmarks_folder()
            newFolder.folder_name = request.POST.get('folder-name')
            newFolder.user = email
            newFolder.save()
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

def PublicationBookmarkInFolder(request, username, folderid, id):
    results = publications.objects.filter(id=id)
    pubID = id
    if(request.user):
        user = request.session['username']
    else:
        user = "null"

    email = request.session['email']
    #bookmark = bookmarks.objects.filter(publicationID=id, user=email)
    annotation = annotations.objects.filter(publicationID=id, author=user)

    rawbookmarks = bookmarks.objects.filter(user=email)
    filterpub = bookmarks.objects.filter(user=email).values('publicationID')
    folders = bookmarks_folder.objects.filter(user=email)
    collaborator = collaborators.objects.filter(owner=email)
    collabs = collaborators.objects.filter(collab=email)

    bookmark = publications.objects.filter(id__in=filterpub)

    collabs = collaborators.objects.filter(collab=email).values('folderID')
    shared_with_me = bookmarks_folder.objects.filter(id__in=collabs)

    next = request.POST.get('next', '/')

    if request.method=='POST':
        if request.POST.get("bookmark_action") == 'add':
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = email
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()
            messages.success(request, "Added to your bookmarks")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'shared':shared_with_me})
        elif request.POST.get("bookmark_action") == 'delete':
            folder_value = request.POST.get('folder_id')
            bookmarks.objects.filter(folderID=folder_value, publicationID=pubID, user=email).delete()

            messages.success(request, "Deleted from your bookmarks")
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'shared':shared_with_me})
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

        elif request.POST.get("newFolder") == 'newFolder':
            newFolder = bookmarks_folder()
            newFolder.folder_name = request.POST.get('folder-name')
            newFolder.user = email
            newFolder.save()
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'shared':shared_with_me})
        else:
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'shared':shared_with_me})
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

        

    else:
         return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs})


def createFolder(request, username):

    email = request.session['email']
    next = request.POST.get('next', '/')

    if request.method == 'POST':
        newFolder = bookmarks_folder()
        newFolder.folder_name = request.POST.get('folder-name')
        newFolder.user = email
        newFolder.save()

        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)


def addCollab(request, username):

    email = request.session['email']
    next = request.POST.get('next', '/')

    if request.method == 'POST':
        newCollab = collaborators()
        newCollab.collab = request.POST.get('email-collab')
        newCollab.owner = email
        newCollab.folderID = request.POST.get('new-folder-id')
        newCollab.save()

        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)

def deleteCollab(request, username):
    email = request.session['email']
    next = request.POST.get('next', '/')

    if request.method == 'POST':
        collab_value = request.POST.get('delete-collab')
        collaborators.objects.get(id=collab_value).delete()

        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)
    
def deleteFolder(request, username):
    email = request.session['email']
    next = request.POST.get('next', '/')

    if request.method == 'POST':
        folder_value = request.POST.get('delete-folder-id')
        annotations.objects.filter(folderID=folder_value).delete()
        bookmarks_folder.objects.get(id=folder_value).delete()
        collaborators.objects.filter(folderID=folder_value).delete()
        bookmarks.objects.filter(folderID=folder_value).delete()
        
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)


def uploadLiterature(request):
        
    if request.method=='POST':
        if(request.user):
            userid = request.session['email']
        else:
            userid = "null"
        if request.POST.get('title') and request.POST.get('author'):
            savepub = publications()
            savepub.title = request.POST.get('title')
            if publications.objects.filter(title=request.POST.get('title')).exists():
                return redirect('upload')
            savepub.abstract = request.POST.get('abstract')
            savepub.author = request.POST.get('author')
            savepub.pdf = request.FILES.get('document')
            savepub.url = 'uploaded'
            savepub.status = 'Pending'
            savepub.source = 'Uploaded'
            savepub.save()
            insert_list = []
            name_id = []
            pub_id = []
            key_id = request.POST.get('keywords').split(",")
            for i in range(0,len(key_id)):
                if keywords.objects.filter(keywordname=key_id[i]):
                    name_id.append(key_id[i])
                else:
                    insert_list.append(keywords(keywordname=key_id[i]))
                    name_id.append(key_id[i])
            keywords.objects.bulk_create(insert_list)
            results = publications.objects.get(title = savepub.title)
            for j in range(0,len(name_id)):
                store = keywords.objects.get(keywordname=name_id[j])
                pub_id.append(pubkeys(publication_id=results.id, keywords_id=store.id))
            pubkeys.objects.bulk_create(pub_id)
            addBookmark = bookmarks()
            addBookmark.user = userid
            addBookmark.publicationID = results.id
            bkfolderid = bookmarks_folder.objects.get(user=userid,folder_name='My Uploads')
            addBookmark.folderID = bkfolderid.id
            addBookmark.save()
            return redirect('/home')#render(request, 'registration/login.html')
        else:
            return render(request, 'upload.html') 
    else:
        return render(request, 'upload.html')
    
def viewAdmin(request):
    results = publications.objects.filter(status='pending')
    if request.method == 'POST':
        if 'Accept' in request.POST.values():
            pair = [key for key in request.POST.keys()][1].split("|")
            stat = publications.objects.get(id=pair[0],title=pair[1])
            stat.status = 'Approved'
            stat.save()
        elif 'Decline' in request.POST.values():
            pair = [key for key in request.POST.keys()][1].split("|")
            #pair will be a list containing x and y
            dec = publications.objects.get(id=pair[0],title=pair[1])
            dec.delete()
            bkmrk = bookmarks.objects.get(publicationID=pair[0])
            bkmrk.delete()

    return render(request, 'main/adminpage.html',{'publications':results})


# def annotateFromPub(request):
#     results = publications.objects.filter(id=id)
#     if request.method=='POST':
#         body= request.POST['annotation']
#         author= request.session['username']
#         pubID = id
#         saveAnnotation = annotations()
#         saveAnnotation.author = author
#         saveAnnotation.body = body
#         saveAnnotation.publicationID = pubID
#         saveAnnotation.save()
#         return render(request, 'publication.html',{'publication':results})