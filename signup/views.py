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
from django.db.models import Q
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
        if request.POST.get('username') and request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name'):
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
            return redirect('/')#render(request, 'registration/login.html')
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
                    Q(author__icontains=searched), source__icontains='ais'
            )


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains='ais') |
                    Q(source__icontains='ieee')
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
                )        


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
                )


            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="ieee"
            )

                
            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
               results = publications.objects.filter(
                    Q(source__icontains="ieee") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
                )


            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="scopus"
            )
            else:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
            )

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0 or '.' not in publication.url or 'https' not in publication.url:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   
                    

            return render(request, 'main/search.html',{'searched':searched, 'results':results})

        elif searchFilter == "title":
            
            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched,source__icontains="ais")


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ais") |
                    Q(source__icontains="ieee"), title__icontains=searched
                )


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ais") |
                    Q(source__icontains="scopus"), title__icontains=searched
                )

                
            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched,source__icontains="ieee")


            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter( 
                    Q(source__icontains="ieee") |
                    Q(source__icontains="scopus"), title__icontains=searched
                )
                
            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(title__icontains=searched, source__icontains="scopus")


            else:
                results = publications.objects.filter(title__icontains=searched)
 

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0 or '.' not in publication.url or 'https' not in publication.url:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   

            return render(request, 'main/search.html',{'searched':searched, 'results':results})

        elif searchFilter == "author":

            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched,source__icontains="ais")


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais")|
                    Q(source__icontains="ieee"), author__icontains=searched
                )


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais")|
                    Q(source__icontains="scopus"), author__icontains=searched
                )


            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched,source__icontains="ieee")


            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ieee")|
                    Q(source__icontains="scopus"), author__icontains=searched
                )

            elif 'scopus' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(author__icontains=searched, source__icontains="scopus")    


            else:
                results = publications.objects.filter(author__icontains=searched)

            

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0 or '.' not in publication.url or 'https' not in publication.url:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()    

            return render(request, 'main/search.html',{'searched':searched, 'results':results})
    else:
        
        pubs = publications.objects.all()
        xlist =     list(pubs)

        for publication in xlist:
            if publication.url == 'doi.org/' or len(publication.url) == 0 or '.' not in publication.url or 'https' not in publication.url:
                publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                publication.save()  

        return render(request, 'main/search.html',{})

def ProfilePage(request, username):

    email = request.session['email']

    rawbookmarks = bookmarks.objects.filter(user=email)
    filterpub = bookmarks.objects.filter(user=email).values('publicationID')
    folders = bookmarks_folder.objects.filter(user=email)


    bookmark = publications.objects.filter(id__in=filterpub)

    return render(request, 'main/profile.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks})

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
    not_bookmark = bookmarks_folder.objects.exclude(id__in=bookmark_value)


    return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'my_folders':my_folders, 'in_bookmark':in_bookmark, 'not_bookmark':not_bookmark})

def PublicationPageAnnotate(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author= request.session['username']
    else:
        author="null"
    annotation = annotations.objects.filter(publicationID=id, author=author)
    next = request.POST.get('next', '/')
    
    if request.method=='POST':
        if 'annotate-add' in request.POST:
            body= request.POST['annotation']
            pubID = id
            saveAnnotation = annotations()
            saveAnnotation.author = author
            saveAnnotation.body = body
            saveAnnotation.publicationID = pubID
            saveAnnotation.save()
            messages.success(request, "Annotation saved")
            return HttpResponseRedirect(next)
        elif 'annotate-save' in request.POST:
            annotation.delete()
            body= request.POST['annotation-exist']
            pubID = id
            saveAnnotation = annotations()
            saveAnnotation.author = author
            saveAnnotation.body = body
            saveAnnotation.publicationID = pubID
            saveAnnotation.save()
            messages.success(request, "Annotation edited")
            return HttpResponseRedirect(next)
        else:
            annotation.delete()
            messages.success(request, "Annotation deleted")
            return HttpResponseRedirect(next)
    else:
        return render(request, 'publication.html', {'publication':results, 'annotations':annotation})

def PublicationBookmark(request, id):
    results = publications.objects.filter(id=id)

    if(request.user):
        user = request.session['username']
    else:
        user = "null"

    email = request.session['email']
    bookmark = bookmarks.objects.filter(publicationID=id, user=email)
    annotation = annotations.objects.filter(publicationID=id, author=user)
    next = request.POST.get('next', '/')

    if request.method=='POST':
        if 'bookmark-add' in request.POST:
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = email
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()
            messages.success(request, "Added to your bookmarks")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return HttpResponseRedirect(next)

        if 'bookmark-delete' in request.POST:
            folder_value = request.POST.get('folder_id')
            bookmarks.objects.filter(folderID=folder_value, publicationID=id, user=email).delete()
            messages.success(request, "Deleted from your bookmarks")
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
        # else:
        #     return HttpResponseRedirect(next)
        #     # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
    else:
        return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

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

    



def uploadLiterature(request):
    if(request.user):
        user = request.session['username']
    else:
        user = "null"
        
    if request.method=='POST':
        if request.POST.get('title') and request.POST.get('author'):
            savepub = publications()
            savepub.title = request.POST.get('title')
            if publications.objects.filter(title=request.POST.get('title')).exists():
                messages.error(request, 'Title already taken', extra_tags='name')
                return redirect('upload')
            savepub.abstract = request.POST.get('abstract')
            savepub.author = request.POST.get('author')
            savepub.pdf = request.FILES.get('document')
            savepub.status = 'Pending'
            savepub.source = 'Uploaded'
            savepub.save()
            insert_list = []
            name_id = []
            pub_id = []
            key_id = request.POST.get('keywords').split(",")
            for i in range(0,len(key_id)-1):
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
            addBookmark.user = user
            addBookmark.publicationID = results.id
            addBookmark.save()
            return redirect('/home')#render(request, 'registration/login.html')
        else:
            return render(request, 'upload.html') 
    else:
        return render(request, 'upload.html')
    
def viewAdmin(request):
    results = publications.objects.filter(status='pending')
    #if request.method == "POST":
        #currpub = publications.objects.filter(id=)

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