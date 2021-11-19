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
    user = request.session['username']
  
    bookmark = bookmarks.objects.filter(user=user).values('publicationID')
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
        
        
        # if 'filterAis' in request.POST:
        #     filterAis = request.POST['filterAis']
        # else:
        #     filterAis = None

        # if 'filterIeee' in request.POST:
        #     filterIeee = request.POST['filterIeee']
        # else:
        #     filterIeee = None

        # if 'filterScopus' in request.POST:
        #     filterScopus = request.POST['filterScopus']
        # else:
        #     filterScopus = None

        libFilter = request.POST.getlist('filterLib')

        if  searchFilter == "default":

            if 'ais' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    # Q(title__icontains=searched) |
                    # Q(author__icontains=searched), source__icontains="ais"
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains='ieee'
            )
            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains='ieee') |
                    Q(source__icontains='scopus')
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
                )
            else:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched)
            )
                
            return render(request, 'main/search.html',{'searched':searched, 'results':results})
        #     elif filterAis is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="ais"
        #         ).filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="scopus"
        #         )
        #     elif filterIeee is not None:
        #         results = publications.objects.filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="ieee"
        #     )
        #     elif filterIeee is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="ieee"
        #         ).filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="scopus"
        #         )
        #     elif filterScopus is not None:
        #         results = publications.objects.filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched), source__icontains="scopus"
        #     )
        #     else:
        #         results = publications.objects.filter(
        #             Q(title__icontains=searched) |
        #             Q(author__icontains=searched)
        #     )

        #     return render(request, 'main/search.html',{'searched':searched, 'results':results})

        # elif searchFilter == "title":
            
           
        #     if filterAis is not None:
        #         results = publications.objects.filter(title__icontains=searched,source__icontains="ais")
        #     elif filterAis is not None and filterIeee is not None:
        #         results = publications.objects.filter( 
        #             title__icontains=searched, source__icontains="ais"
        #         ).filter(
        #             title__icontains=searched, source__icontains="ieee"
        #         )
        #     elif filterAis is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             title__icontains=searched, source__icontains="ais"
        #         ).filter(
        #             title__icontains=searched, source__icontains="scopus"
        #         )
        #     elif filterIeee is not None:
        #         results = publications.objects.filter(title__icontains=searched,source__icontains="ieee")
        #     elif filterIeee is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             title__icontains=searched, source__icontains="ieee"
        #         ).filter(
        #             title__icontains=searched, source__icontains="scopus"
        #         )
        #     elif filterScopus is not None:
        #         results = publications.objects.filter(title__icontains=searched, source__icontains="scopus")
        #     else:
        #         results = publications.objects.filter(title__icontains=searched)

        #     return render(request, 'main/search.html',{'searched':searched, 'results':results})
        # elif searchFilter == "author":

        #     if filterAis is not None:
        #         results = publications.objects.filter(author__icontains=searched,source__icontains="ais")
        #     elif filterAis is not None and filterIeee is not None:
        #         results = publications.objects.filter(
        #             author__icontains=searched,source__icontains="ais"
        #         ).filter(
        #             author__icontains=searched,source__icontains="ieee"
        #         )
        #     elif filterAis is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             author__icontains=searched,source__icontains="ais"
        #         ).filter(
        #             author__icontains=searched,source__icontains="scopus"
        #         )
        #     elif filterIeee is not None:
        #         results = publications.objects.filter(author__icontains=searched,source__icontains="ieee")
        #     elif filterIeee is not None and filterScopus is not None:
        #         results = publications.objects.filter(
        #             author__icontains=searched,source__icontains="ieee"
        #         ).filter(
        #             author__icontains=searched,source__icontains="scopus"
        #         )
        #     elif filterScopus is not None:
        #         results = publications.objects.filter(author__icontains=searched, source__icontains="scopus")    
        #     else:
        #         results = publications.objects.filter(author__icontains=searched)
        #     return render(request, 'main/search.html',{'searched':searched, 'results':results})
    else:
        return render(request, 'main/search.html',{})

#this function displays the details of a publication that has been selected from the home page
def PublicationPage(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author = request.session['username']
    else:
        author="null"
    annotation = annotations.objects.filter(publicationID=id, author=author)
    bookmark = bookmarks.objects.filter(publicationID=id, user=author)
    return render(request, 'publication.html', {'publication':results, 'annotations':annotation, 'bookmarks':bookmark})

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

    bookmark = bookmarks.objects.filter(publicationID=id, user=user)
    annotation = annotations.objects.filter(publicationID=id, author=user)
    next = request.POST.get('next', '/')

    if request.method=='POST':
        if 'bookmark-add' in request.POST:
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = user
            addBookmark.publicationID = pubID
            addBookmark.save()
            messages.success(request, "Added to your bookmarks")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return HttpResponseRedirect(next)
        elif 'bookmark-delete' in request.POST:
            bookmark.delete()
            messages.success(request, "Deleted from your bookmarks")
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
        else:
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
    else:
        return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})


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