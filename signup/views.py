from django.core import paginator
from django.db import reset_queries
from django.db.models.fields import EmailField, NullBooleanField
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from reportlab.lib import fonts, pagesizes
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
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4, LEGAL, landscape, letter
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.platypus import Paragraph, Table, TableStyle
import requests
from bs4 import BeautifulSoup
import operator
from collections import Counter
import time
import re
import json
import urllib
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize

# Create your views here.

def index(request):

    return render(request, 'main/index.html')

def home(request):
    results = publications.objects.all()
    annotation = annotations.objects.all()
    publication_keys = pubkeys.objects.all()
    
    # for publication in list(results):
    #     flag = 0
    #     for pubkey in publication_keys:
    #         if publication.id == pubkey.publication_id and flag == 0:
    #             flag=1
    #     if flag == 0:
    #         if "http" in publication.url: 
    #             scrap(publication.url, publication.id)
    #         else:
    #             scrap("http://" + publication.url, publication.id)

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
            bookmarks_folder.objects.bulk_create([
                bookmarks_folder(folder_name='My Uploads',user=request.POST.get('email')),
                bookmarks_folder(folder_name='My Bookmarks',user=request.POST.get('email'))
            ])
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


def scrap(url, id): 
  
    # empty list to store the contents of  
    # the website fetched from our web-crawler 
    wordlist = [] 
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    
    
    source_code=''
    try:
        source_code = requests.get(url).text
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    

    # BeautifulSoup object which will 
    # ping the requested url for data 
    soup = BeautifulSoup(source_code, 'html.parser') 
  
    # Text in given web-page is stored under 
    # the <div> tags with class <entry-content> 

    if "aisel" in url:
        table = soup.findAll('div', {'id':'abstract'})
        for x in table:
            content = x.find('p').text
    
            # use split() to break the sentence into  
            # words and convert them into lowercase  
            words = content.lower().split() 
            
            for each_word in words: 
                wordlist.append(each_word) 
            clean_wordlist(wordlist, id)
    elif "ieeexplore" in url:

        ieee_content = requests.get(url, timeout=180)
        soup = BeautifulSoup(ieee_content.content, "html.parser")
        scripts = soup.find_all("script")
        
        pattern = re.compile(r"(?<=\"keywords\":)\[{.*?}\]")
        keywords_dict = {}
        for i, script in enumerate(scripts):
            keywordslist = re.findall(pattern, str(script.string))
            if len(keywordslist) == 1:
                raw_keywords_list = json.loads(keywordslist[0])
                
                for index, keyword_type in enumerate(raw_keywords_list):
                    if "type" in raw_keywords_list[index]:
                        keywords_dict[keyword_type["type"].strip()] = [kwd.strip() for kwd in keyword_type["kwd"]]
        
        if 'Author Keywords' in keywords_dict:
            if len(list(keywords_dict['Author Keywords'])) > 0:

                newkeywords = []
                name_id= []
                insert_list = []
                pub_id = []
                filtered =[]
                top = list(keywords_dict['Author Keywords'])

                for word in top:
                    newkeywords.append(word)

                filtered = [word for word in newkeywords if not word in stopwords.words()]
                filtered_dupes = []
                for i in list(filtered):
                    if i.lower() not in filtered_dupes:
                        filtered_dupes.append(i)

                for i in range(0,len(filtered_dupes)):
                    if keywords.objects.filter(keywordname=filtered_dupes[i].strip()):
                        name_id.append(filtered_dupes[i].strip())
                    else:
                        insert_list.append(keywords(keywordname=filtered_dupes[i].strip()))
                        name_id.append(filtered_dupes[i].strip())

                print(url, flush=True)
                print(filtered)
                print(filtered_dupes)
                keywords.objects.bulk_create(insert_list)

            
                for j in range(0,len(name_id)):
                    store = keywords.objects.get(keywordname=name_id[j])
                    pub_id.append(pubkeys(publication_id=id, keywords_id=store.id))
                pubkeys.objects.bulk_create(pub_id)
        else:
            web_page = url
            page = urllib.request.urlopen(web_page)
            soup = BeautifulSoup(page, 'lxml')        
            abstract = soup.find("meta", property="og:description")
                
            words = str(abstract).lower().split() 
                    
            for each_word in words: 
                wordlist.append(each_word) 
            clean_wordlist(wordlist, id)

                
            


def clean_wordlist(wordlist, id): 
      
    clean_list =[] 
    for word in wordlist: 
        symbols = '!@#$%^&*()_-+={[}]|;:"<>?/.,\- '
          
        for i in range (0, len(symbols)): 
            word = word.replace(symbols[i], '') 
              
        if len(word) > 0: 
            clean_list.append(word) 
    create_dictionary(clean_list,id)


def create_dictionary(clean_list, id): 
    word_count = {} 
      
    for word in clean_list: 
        if word in word_count: 
            word_count[word] += 1
        else: 
            word_count[word] = 1
  
      
    c = Counter(word_count) 
      
    # returns the most occuring elements 
    top = c.most_common(20) 
    
    newkeywords = []
    name_id= []
    insert_list = []
    pub_id = []
    filtered =[]

    

    for word in top:
        newkeywords.append(word[0])

    filtered = [word for word in newkeywords if not word in stopwords.words()]

    
    for i in range(0,len(filtered)):
        if keywords.objects.filter(keywordname=filtered[i].strip()):
            name_id.append(filtered[i].strip())
        else:
            insert_list.append(keywords(keywordname=filtered[i].strip()))
            name_id.append(filtered[i].strip())

    keywords.objects.bulk_create(insert_list)

        
    for j in range(0,len(name_id)):
        store = keywords.objects.get(keywordname=name_id[j])
        pub_id.append(pubkeys(publication_id=id, keywords_id=store.id))
    pubkeys.objects.bulk_create(pub_id)




def searchPublication(request):
    if request.method == "GET":
        # searched = request.POST['searched']
        # searchFilter = request.POST['filterData']
        
        # libFilter = request.POST.getlist('filterLib')

        searched = request.GET.get('searched','')
        searchFilter = request.GET.get('filterData','')
        libFilter = request.GET['filterLib']

        if (request.user):
            author = request.session['username']
        else:
            author="null"

        email = request.session['email']

        my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
        my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

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

            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            keyword_count = []
            

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)
                                

            page_results = Paginator(results, 10)
            page_number = 1
            page_obj = page_results.get_page(page_number)      

            # for publication in xlist:
            #     flag = 0
            #     for pubkey in publication_keys:
            #         if publication.id == pubkey.publication_id and flag == 0:
            #             flag=1
            #     if flag == 0:
            #         if "http" in publication.url: 
            #             scrap(publication.url, publication.id)
            #         else:
            #             scrap("http://" + publication.url, publication.id)

            filteredYear =[]
            for year in xlist:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()

            print(len(keyword_results))
            return render(request, 'main/search.html',{'searched':searched, 'results':results, 'keyword_results':keyword_results, 'bookmarks': my_bookmarks_folder_contents, 'my_bookmarks_id': my_bookmarks_folder, 'filteredYear': filteredYear})

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
            
            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            keyword_count = []

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)

            for publication in xlist:
                flag = 0
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id and flag == 0:
                        flag=1
                if flag == 0:
                    if "http" in publication.url: 
                        scrap(publication.url, publication.id)
                    else:
                        scrap("http://" + publication.url, publication.id)

            filteredYear =[]
            for year in xlist:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()


            return render(request, 'main/search.html',{'searched':searched, 'results':results, 'keyword_results':keyword_results, 'bookmarks': my_bookmarks_folder_contents, 'my_bookmarks_id': my_bookmarks_folder, 'filteredYear': filteredYear})

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

            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            keyword_count = []

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname) 

            for publication in xlist:
                flag = 0
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id and flag == 0:
                        flag=1
                if flag == 0:
                    if "http" in publication.url: 
                        scrap(publication.url, publication.id)
                    else:
                        scrap("http://" + publication.url, publication.id)

            filteredYear =[]
            for year in xlist:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()
            return render(request, 'main/search.html',{'searched':searched, 'results':results, 'keyword_results':keyword_results, 'bookmarks': my_bookmarks_folder_contents, 'my_bookmarks_id': my_bookmarks_folder, 'filteredYear': filteredYear})
    else:
        
        pubs = publications.objects.all()
        xlist =     list(pubs)

        for publication in xlist:
            if publication.url == 'doi.org/' or len(publication.url) == 0:
                publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                publication.save()

        publication_keys = pubkeys.objects.all()
        keywords_list = keywords.objects.all()
        keyword_results = []
        keyword_count = []

        for publication in xlist:
            for pubkey in publication_keys:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubid.keywordname not in keyword_results:
                                keyword_results.append(pubid.keywordname)  

        for publication in xlist:
                flag = 0
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id and flag == 0:
                        flag=1
                if flag == 0:
                    if "http" in publication.url: 
                        scrap(publication.url, publication.id)
                    else:
                        scrap("http://" + publication.url, publication.id)

        return render(request, 'main/search.html',{ 'keyword_results':keyword_results})

def filterSearch(request, filter, search):
    
        searched = search
        
        if filter.isnumeric():
            results = publications.objects.filter(title__icontains=searched, status__icontains="approved", year__icontains=filter)

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   

            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            keyword_count = []

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)

            return render(request, 'main/search-filter.html',{'searched':search, 'results':results, 'keyword_results':keyword_results})

        else:
            results = publications.objects.filter(title__icontains=searched, status__icontains="approved", year__icontains=filter)

            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()   

            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            keyword_count = []

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)

            return render(request, 'main/search-filter.html',{'searched':search, 'results':results, 'keyword_results':keyword_results})

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
    shared_folders_bookmarks = bookmarks.objects.filter(folderID__in=shared_folders_ids) #Get all bookmarks that have collaborators
    shared_folders_pubs = publications.objects.filter(id__in=shared_folders_bookmarks.values('publicationID')) #Get the publications that are shared
    
    return render(request, 'main/my-folders.html',{'bookmarks':bookmark,
                                                    'folders':folders,
                                                    'rawbookmarks':rawbookmarks,
                                                    'collaborators':collaborator,
                                                    'collabs':collabs,
                                                    'sharedfolders': shared_folders,
                                                    'sharedbookmarks': shared_folders_bookmarks,
                                                    'sharedpubs':shared_folders_pubs})

#this function displays the details of a publication that has been selected from the home page
def PublicationPage(request, id):
    results = publications.objects.filter(id=id)
    if (request.user):
        author = request.session['username']
    else:
        author="null"

    email = request.session['email']

    annotation = annotations.objects.filter(publicationID=id, author=author)
    collaborator = collaborators.objects.filter(owner=email)


    my_folders = bookmarks_folder.objects.filter(user=email)
    folders_value = bookmarks_folder.objects.filter(user=email).values('id')

    bookmark_value = bookmarks.objects.filter(publicationID=id, folderID__in=folders_value).values('folderID')


    in_bookmark = bookmarks_folder.objects.filter(id__in=bookmark_value)
    not_bookmark = bookmarks_folder.objects.exclude(id__in=bookmark_value).filter(id__in=folders_value)

    my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
    my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

    if my_bookmarks_folder_contents.filter(publicationID=id):
        in_my_bookmarks = 'true'
    else: in_my_bookmarks = 'false'

    collabs = collaborators.objects.filter(collab=email).values('folderID') #Get the folderIDs of the folders that have collaborators
    shared_folders = bookmarks_folder.objects.filter(id__in=collabs) #The folders that have collaborators

    shared_folders_ids = bookmarks_folder.objects.filter(id__in=collabs).values('id') #Get the ids of the folders that have collaborators
    shared_folders_bookmarks = bookmarks.objects.filter(folderID__in=shared_folders_ids, publicationID=id) #Get all bookmarks that have collaborators
    shared_folders_pubs = publications.objects.filter(id__in=shared_folders_bookmarks.values('publicationID')) #Get the publications that are shared

    in_shared_bookmark = bookmarks_folder.objects.filter(id__in=shared_folders_bookmarks.values('folderID'))
    not_shared_bookmark = bookmarks_folder.objects.exclude(id__in=shared_folders_bookmarks.values('folderID')).filter(id__in=collabs)

    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()
    keyword_results = []
    keyword_count = []
    xlist = list(results)

    for publication in xlist:
        for pubkey in publication_keys:
            if publication.id == pubkey.publication_id:
                for pubid in keywords_list:
                    if pubkey.keywords_id == pubid.id:
                        if pubid.keywordname not in keyword_results:
                            keyword_results.append(pubid.keywordname) 

    return render(request, 'publication.html', {'publication':results,
                                                'annotations':annotation,
                                                'my_folders':my_folders, 
                                                'in_bookmark':in_bookmark, 
                                                'not_bookmark':not_bookmark, 
                                                'pubID': id, 
                                                'collaborators':collaborator, 
                                                'collabs':collabs, 
                                                'sharedfolders': shared_folders, 
                                                'sharedbookmarks': shared_folders_bookmarks, 
                                                'sharedpubs':shared_folders_pubs, 
                                                'inshared':in_shared_bookmark, 
                                                'notinshared':not_shared_bookmark, 
                                                'keyword_results':keyword_results, 
                                                'bool_in_bookmark': in_my_bookmarks,
                                                'my_bookmarks_id': my_bookmarks_folder,
                                                'my_bookmarks_content':my_bookmarks_folder_contents})

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

    my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
    my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

    if my_bookmarks_folder_contents.filter(publicationID=id):
        in_my_bookmarks = 'true'
    else: in_my_bookmarks = 'false'

    collabs = collaborators.objects.filter(collab=email).values('folderID') #Get the folderIDs of the folders that have collaborators
    shared_folders = bookmarks_folder.objects.filter(id__in=collabs) #The folders that have collaborators

    shared_folders_ids = bookmarks_folder.objects.filter(id__in=collabs).values('id') #Get the ids of the folders that have collaborators
    shared_folders_bookmarks = bookmarks.objects.filter(folderID__in=shared_folders_ids) #Get all bookmarks that have collaborators
    shared_folders_pubs = publications.objects.filter(id__in=shared_folders_bookmarks.values('publicationID')) #Get the publications that are shared

    in_shared_bookmark = bookmarks_folder.objects.filter(id__in=shared_folders_bookmarks.values('folderID'))
    not_shared_bookmark = bookmarks_folder.objects.exclude(id__in=shared_folders_bookmarks.values('folderID')).filter(id__in=collabs)

    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()
    keyword_results = []
    keyword_count = []
    xlist = list(results)

    for publication in xlist:
        for pubkey in publication_keys:
            if publication.id == pubkey.publication_id:
                for pubid in keywords_list:
                    if pubkey.keywords_id == pubid.id:
                        if pubid.keywordname not in keyword_results:
                            keyword_results.append(pubid.keywordname)

    return render(request, 'publication-folder.html', {'publication':results,
                                                       'annotations':annotation,
                                                       'my_folders':my_folders,
                                                       'in_bookmark':in_bookmark,
                                                       'not_bookmark':not_bookmark,
                                                       'folderID': folderid,
                                                       'pubID': id,
                                                       'collaborators':collaborator,
                                                       'collabs':collabs,
                                                       'sharedfolders': shared_folders,
                                                       'sharedbookmarks': shared_folders_bookmarks,
                                                       'sharedpubs':shared_folders_pubs,
                                                       'inshared':in_shared_bookmark,
                                                       'notinshared':not_shared_bookmark,
                                                       'keyword_results':keyword_results,
                                                        'bool_in_bookmark': in_my_bookmarks,
                                                        'my_bookmarks_id': my_bookmarks_folder,
                                                        'my_bookmarks_content':my_bookmarks_folder_contents})


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
            saveAnnotation.isEdited = 0
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
            saveAnnotation.isEdited = 1
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
            messages.success(request, "Added to your folder")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return HttpResponseRedirect(next)
        elif request.POST.get("bookmark_action") == 'delete':
            folder_value = request.POST.get('folder_id')
            bookmarks.objects.filter(folderID=folder_value, publicationID=pubID, user=email).delete()

            messages.success(request, "Deleted from your folder")
            return HttpResponseRedirect(next)
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
        elif request.POST.get("bookmark_action") == 'sharedAdd':

            folderOwner = bookmarks_folder.objects.get(id=request.POST.get('folder_id'))
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = folderOwner.user
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()


            messages.success(request, "Added to shared folder")
            return HttpResponseRedirect(next)
        elif request.POST.get("bookmark_action") == 'sharedDelete':
            folder_value = request.POST.get('folder_id')
            folderOwner = bookmarks_folder.objects.get(id=request.POST.get('folder_id'))
            bookmarks.objects.filter(folderID=folder_value, publicationID=pubID, user=folderOwner.user).delete()

            messages.success(request, "Deleted from shared folder")
            return HttpResponseRedirect(next)
        
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

    bookmark = publications.objects.filter(id__in=filterpub)

    collabs = collaborators.objects.filter(collab=email).values('folderID') #Get the folderIDs of the folders that have collaborators
    shared_folders = bookmarks_folder.objects.filter(id__in=collabs) #The folders that have collaborators

    shared_folders_ids = bookmarks_folder.objects.filter(id__in=collabs).values('id') #Get the ids of the folders that have collaborators
    shared_folders_bookmarks = bookmarks.objects.filter(folderID__in=shared_folders_ids) #Get all bookmarks that have collaborators
    shared_folders_pubs = publications.objects.filter(id__in=shared_folders_bookmarks.values('publicationID')) #Get the publications that are shared

    next = request.POST.get('next', '/')

    if request.method=='POST':
        if request.POST.get("bookmark_action") == 'add':
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = email
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()
            # messages.success(request, "Added to your bookmarks")

            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedbookmarks': shared_folders_bookmarks, 'sharedpubs':shared_folders_pubs})
        elif request.POST.get("bookmark_action") == 'delete':
            folder_value = request.POST.get('folder_id')
            bookmarks.objects.filter(folderID=folder_value, publicationID=pubID, user=email).delete()

            # messages.success(request, "Deleted from your bookmarks")
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedbookmarks': shared_folders_bookmarks, 'sharedpubs':shared_folders_pubs})
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

        elif request.POST.get("newFolder") == 'newFolder':
            newFolder = bookmarks_folder()
            newFolder.folder_name = request.POST.get('folder-name')
            newFolder.user = email
            newFolder.save()
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedbookmarks': shared_folders_bookmarks, 'sharedpubs':shared_folders_pubs})
        else:
            return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedbookmarks': shared_folders_bookmarks, 'sharedpubs':shared_folders_pubs})
            # return render(request, 'publication.html', {'publication':results, 'bookmarks':bookmark, 'annotations':annotation})

        

    else:
         return render(request, 'main/my-folders.html',{'bookmarks':bookmark, 'folders':folders, 'rawbookmarks':rawbookmarks, 'collaborators':collaborator, 'collabs':collabs, 'sharedfolders': shared_folders, 'sharedbookmarks': shared_folders_bookmarks, 'sharedpubs':shared_folders_pubs})


def createFolder(request, username):

    email = request.session['email']
    name = request.POST.get('folder-name')
    next = request.POST.get('next', '/')

    if request.method == 'POST':
        newFolder = bookmarks_folder()
        newFolder.folder_name = name.capitalize()
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
                return render(request, 'upload.html', {'some_flag': True})
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
                if keywords.objects.filter(keywordname=key_id[i].strip()):
                    name_id.append(key_id[i].strip())
                else:
                    insert_list.append(keywords(keywordname=key_id[i].strip()))
                    name_id.append(key_id[i].strip())
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

def myTable(tabledata):

    from reportlab.platypus.flowables import KeepTogether
    from reportlab.lib.units import mm
    # List of Lists
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_LEFT

    table = Table(tabledata, colWidths=(45*mm, 45*mm, 45*mm, 25*mm, 20*mm))
    # add style
    style = TableStyle([
        ('BACKGROUND', (0,1), (4,1), colors.green),
        ('TEXTCOLOR',(0,1),(4,1),colors.whitesmoke),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        ('FONTNAME', (0,1), (4,1), 'Courier-Bold'),
        ('FONTSIZE', (0,1), (4,1), 14),
        ('FONTSIZE', (0,0), (4,0), 16),
        ('BOTTOMPADDING', (0,0), (4,0), 15),
        ('BOTTOMPADDING', (0,1), (4,1), 12),
        #('BACKGROUND',(0,1),(-1,-1),colors.beige),
            
    ])
    table.setStyle(style)
    # 2) Alternate backgroud color
    rowNumb = len(tabledata)
    for i in range(2, rowNumb):
        if i % 2 != 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
            
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,1),(-1,-1),2,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),
            ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )
        table.setStyle(ts)
    return table

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Spacer, Image, Table, TableStyle, SimpleDocTemplate
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.legends import Legend

#create a bar chart and specify positions, sizes, and colors

#add a legend for the bar chart

def downloadFolderTable(request):
    email = request.session['email']
    if request.method == 'POST':
        pair = [key for key in request.POST.keys()][1].split("|")
        filterpub = bookmarks.objects.filter(user=email,folderID=pair[0]).values('publicationID')
        getpubs = publications.objects.filter(id__in=filterpub)
        from reportlab.platypus.flowables import KeepTogether
        from reportlab.lib.units import mm
        # List of Lists
        buf = io.BytesIO()
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        title_style = styles['Heading1']
        title_style.alignment = TA_CENTER
        title_style.fontSize=24
        styleN.alignment = TA_LEFT
        ptext = "This is an example."
        can = canvas.Canvas(buf, pagesize=A4)
        p = Paragraph(ptext, style=styles["Normal"])
        p.wrapOn(can, 50*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
        p.drawOn(can, 0*mm, 0*mm)
        can.save()
        
        data = [
            ['Title', 'Author', 'URL', 'Source', 'Year']
        ]
        
        for pub in getpubs:
            data.append([Paragraph(pub.title, styleN),Paragraph(pub.author, styleN),Paragraph(pub.url, styleN),Paragraph(pub.source, styleN),Paragraph(pub.year, styleN)])
            #data.append([KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN))])
            #data.append([Paragraph(pub.title,styles['Normal']),pub.author,'Title','Title','Title','Title'])
        
        pdf = SimpleDocTemplate(
            buf,
            pagesize=A4,
            format=landscape
        )

        idata = [3, 18]

        from reportlab.lib.validators import Auto
        from reportlab.graphics.charts.piecharts import Pie

        chart = Pie()
        chart.data = idata
        chart.x = 50
        chart.y = 5

        lab = []

        for pub in getpubs:
            lab.append(pub.source)

        chart.labels = lab
        chart.sideLabels = True

        chart.slices[0].fillColor = colors.red
        chart.slices[0].popout = 8

        title = String(
            50, 110, 
            'Source Chart', 
            fontSize = 14
        )	

        legend = Legend()
        legend.x = 180
        legend.y = 80
        legend.alignment = 'right' 	

        legend.colorNamePairs = Auto(obj=chart)

        drawing = Drawing(240, 120)
        drawing.add(title)
        drawing.add(chart)
        drawing.add(legend)

        table = Table(data, colWidths=(45*mm, 45*mm, 45*mm, 25*mm, 20*mm))
        # add style
        style = TableStyle([
            ('BACKGROUND', (0,0), (4,0), colors.green),
            ('TEXTCOLOR',(0,0),(4,0),colors.whitesmoke),

            ('ALIGN',(0,0),(-1,-1),'CENTER'),

            ('VALIGN', (0, 0), (-1, -1), 'TOP'),

            ('FONTNAME', (0,0), (4,0), 'Courier-Bold'),
            ('FONTSIZE', (0,0), (4,0), 14),
            ('FONTSIZE', (0,0), (4,0), 16),
            ('BOTTOMPADDING', (0,0), (4,0), 15),
            ('BOTTOMPADDING', (0,0), (4,1), 12),
            #('BACKGROUND',(0,1),(-1,-1),colors.beige),
            
        ])
        table.setStyle(style)
        # 2) Alternate backgroud color
        rowNumb = len(data)
        for i in range(2, rowNumb):
            if i % 2 != 0:
                bc = colors.burlywood
            else:
                bc = colors.beige
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,0),(-1,-1),1,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),1,colors.red),
            ('LINEABOVE',(0,2),(-1,2),1,colors.green),
            ('GRID',(0,0),(-1,-1),1,colors.black),
            ]
        )
        from reportlab.platypus import  Spacer
        table.setStyle(ts)
        elems = []
        elems.append(Paragraph("<strong>Summary for </strong>" + pair[1],title_style))
        elems.append(Spacer(1,.25*inch))
        elems.append(KeepTogether(table))
        elems.append(Spacer(1,.25*inch))
        drawing.hAlign = 'CENTER'
        elems.append(drawing)
        #elems.append(d)
        pdf.build(elems)
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='Corpus_Table.pdf')

'''
#This is your data collected from your Vizard experiment

#take the data and make ready for paragraph
def dataToParagraph(data):
   
    p = '<strong>Subject name: </strong>' + data + '<br/>' + '<strong>Data: </strong>  ('
    for i in range(len(data)):
        p += str(data[i])
        if i != len(data) - 1:
            p += ', '
        else:
            p += ')'   
    return p

#take the data and convert to list of strings ready for table
def dataToTable(name, data):
   
    data = [str(x) for x in data]
    data.insert(0,name)
    return data


#create the table for our document
def myTable(tabledata):

    from reportlab.platypus.flowables import KeepTogether
    from reportlab.lib.units import mm
    # List of Lists
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    styleN.alignment = TA_LEFT

    table = Table(tabledata, colWidths=(45*mm, 45*mm, 45*mm, 25*mm, 20*mm))
    # add style
    style = TableStyle([
        ('BACKGROUND', (0,1), (4,1), colors.green),
        ('TEXTCOLOR',(0,1),(4,1),colors.whitesmoke),

        ('ALIGN',(0,0),(-1,-1),'CENTER'),

        ('VALIGN', (0, 0), (-1, -1), 'TOP'),

        ('FONTNAME', (0,1), (4,1), 'Courier-Bold'),
        ('FONTSIZE', (0,1), (4,1), 14),
        ('FONTSIZE', (0,0), (4,0), 16),
        ('BOTTOMPADDING', (0,0), (4,0), 15),
        ('BOTTOMPADDING', (0,1), (4,1), 12),
        #('BACKGROUND',(0,1),(-1,-1),colors.beige),
            
    ])
    table.setStyle(style)
    # 2) Alternate backgroud color
    rowNumb = len(tabledata)
    for i in range(2, rowNumb):
        if i % 2 != 0:
            bc = colors.burlywood
        else:
            bc = colors.beige
            
        ts = TableStyle(
            [('BACKGROUND', (0,i),(-1,i), bc)]
        )
        table.setStyle(ts)
        # 3) Add borders
        ts = TableStyle(
            [
            ('BOX',(0,1),(-1,-1),2,colors.black),
            ('LINEBEFORE',(2,1),(2,-1),2,colors.red),
            ('LINEABOVE',(0,2),(-1,2),2,colors.green),
            ('GRID',(0,1),(-1,-1),2,colors.black),
            ]
        )
        table.setStyle(ts)
    return table

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Spacer, Image, Table, TableStyle, SimpleDocTemplate
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.textlabels import Label
from reportlab.graphics.charts.legends import Legend

#create a bar chart and specify positions, sizes, and colors
def myBarChart(data):
    drawing = Drawing(400, 200)
    
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 125
    bc.width = 300
    bc.data = data
    bc.barWidth = .3*inch
    bc.groupSpacing = .2 * inch

    bc.strokeColor = colors.black

    bc.valueAxis.valueMin = 0
    bc.valueAxis.valueMax = 100
    bc.valueAxis.valueStep = 10

    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.categoryAxis.labels.dx = 8
    bc.categoryAxis.labels.dy = -2

    bc.categoryAxis.categoryNames = ['Trial1', 'Trial2', 'Trial3', 'Trial4', 'Trial5']

    bc.bars[0].fillColor = colors.blue
    bc.bars[1].fillColor = colors.lightblue

 
    drawing.add(bc)

    return drawing

#add a legend for the bar chart
def myBarLegend(drawing, name1, name2):
    "Add sample swatches to a diagram."

    d = drawing or Drawing(400, 200)

    swatches = Legend()
    swatches.alignment = 'right'
    swatches.x = 80
    swatches.y = 160
    swatches.deltax = 60
    swatches.dxTextSpace = 10
    swatches.columnMaximum = 4
    items = [(colors.blue, name1), (colors.lightblue, name2)]
    swatches.colorNamePairs = items

    d.add(swatches, 'legend')
    return d


########   Now lets put everything together.   ########

# create a list and add the elements of our document (image, paragraphs, table, chart) to it
def downloadFolderTable(request):
    story = []

    #define the style for our paragraph text
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    #First add the Vizard Logo
    #im = Image("dlsu_green.png", width=3*inch, height=3*inch)
    #im.hAlign = 'CENTER'
    #story.append(im)

    #add the title
    email = request.session['email']
    pair = [key for key in request.POST.keys()][1].split("|")
    story.append(Paragraph("<strong>Results for </strong>" + pair[1],styleN))
    story.append(Spacer(1,.25*inch))

    #convert data to paragraph form and then add paragraphs

    #add our table - first prepare data and then pass this to myTable function
    filterpub = bookmarks.objects.filter(user=email,folderID=pair[0]).values('publicationID')
    getpubs = publications.objects.filter(id__in=filterpub)
    tabledata = [
        ['Title', 'Author', 'URL', 'Source', 'Year']
    ]
        
    for pub in getpubs:
        tabledata.append([Paragraph(pub.title, styleN),Paragraph(pub.author, styleN),Paragraph(pub.url, styleN),Paragraph(pub.source, styleN),Paragraph(pub.year, styleN)])
        #data.append([KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN))])
        #data.append([Paragraph(pub.title,styles['Normal']),pub.author,'Title','Title','Title','Title'])

    story.append(myTable(tabledata))
    story.append(Spacer(1,.5*inch))

    #add our barchart and legend
    #drawing = myBarChart([results1,results2])
    #drawing = myBarLegend(drawing,subject1,subject2)
    #drawing.hAlign = 'CENTER'
    #story.append(drawing)

    #build our document with the list of flowables we put together
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf ,pagesize = letter, topMargin=0)
    doc.build(story)
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Corpus_Table.pdf')
'''
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