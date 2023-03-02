from email.quoprimime import decode
from enum import unique
from django.core import paginator
from django.db import reset_queries
from django.db.models.fields import EmailField, NullBooleanField
from django.db.models.query_utils import FilteredRelation
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from reportlab.lib import fonts, pagesizes
from .models import pubkeys, records_bookmark, records_center_uploads, records_search, records_view_publication, records_view_tag, registerUser
from .models import publications
from .models import keywords
from .models import annotations
from .models import bookmarks
from .models import bookmarks_folder
from .models import collaborators
from datetime import datetime
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import time
import datetime
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
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import operator
from collections import Counter
import time
import re
import json
import urllib
from difflib import SequenceMatcher
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from requests.exceptions import ConnectionError
from collections import Counter
from django.urls import resolve
from urllib.parse import urlencode
from django import template
from django.template import *
import random
import re
import fnmatch
import mimetypes
from django.contrib.auth.hashers import make_password, check_password
# from .forms import PostForm
from tablib import Dataset
from .resources import PublicationResource
from django.db.models import Q

#stopwords to be removed from scaping
all_stopwords = stopwords.words('english')
newStopWords = ['div', 'divdiv', 'scholaradivdivdivdivdivdiv', 'classrowdiv', 'scholarapdiv', 'use', 'div', 'td', 'li', 'ul', 'meta', 'function','var', 'start', 'inner', 'end', 'lia', 'span'
'script', 'true', 'tr', 'null', '0', 'input', 'p', 'tabindex1',  'islandsoption', 'section', 'sections', 'classreferencessuffixa', 'classsimpletooltipblockb', 'classxa', 'referencesitemxa', 
'classgooglescholar', 'classvisibilityhiddengoogle', 'scholarspanimg', 'srcspecsproductsacmimagesgooglescholarsvg', 'altgoogle', 'ariahiddentrue', 'typetextjavascript', 'charsetutf8script'
'scholaraspanspan', 'targetblankspan', 'classvisibilityhiddendigital', 'classwidget', 'widgetnone', 'classwrapped', 'classwidgetbody', 'bodynone', 'widgetcompactall', 'bodycompactalldiv', 
'datatrackclick', 'datatracklabellink', 'datatrackactionoutbound', 'namecitationreference', 'classcarticlereferencesitem', 'jscreadingcompanionreferencesitemspan', 'classcarticlereferencestext'
'uhideprinta', 'classcarticlereferenceslinks', 'arialabelgoogle', 'classcitauthspan','classcitrefsprinkles', 'html', 'HTML', 'xhtmlspam', 'htmlheadscript', 'contenttexthtml', '100', 'margin'
'02', '015s', 'fontsize', '16px', 'ct', 'libraryspanimg', 'datatitledigital', 'targetblank', 'relnoopener', 'classoccurrence', 'classcitationdiv', 'classcitationcontent', 'classoccurrencesspan'
'occurrencegsa', 'classgooglescholarlink', 'gtmreference', 'scholarspanspanaspanspandivlili', 'htmlbodyh1403', 'forbiddenh1', 'bodyhtml', 'ietfdtd', '20en', 'htmlhead', 'title403', 'forbiddentitle',
'headbody', 'h1forbiddenh1', 'href', 'classrlist', 'bodyhtml', 'target''blank''img', 'classfootersu003eu003ca', 'classfootersa', 'u003cspan', 'class''reflink''', 'xmlnsxlinkhttpwwww3org1999xlinkgtuqmathrm',
'767px', 'width', 'classarticle', 'th', 'table',  'tr', 'img', 'url', 'alignright', 'styleverticalalign', 'superregspan', 'u003cspan', '—', '�����', '�', '��','srcincapsularesourcecwudnsai1xinfo1275682121020nnny20rt2816407176583692002920q2802012012012920r2812012920b1528142c02c02920u18incidentid1432000850098955416302543539443078476edet15cinfo0e000000e683rpinfo0mthget',
'���', '�', 'filterflatedecodelength', 'filterflatedecodefirst', '792mediabox0', '792parent','�', 'stylebackgroundcolorf5f5f5boxshadownonepa', 'databackgroundf5f5f5', 'classreferencescopy2a', 
'10px', 'teaseritemtitlexa', 'classteaseritema', 'fillcurrentcolor', 'classcitationlink', 'classpanelpane', 'classpanecontent', 'navbarlight', 'navbarnav', 'layerbylayer', 'typehidden', 'pagename', 'classpanelpane',
'colspan2',  'rfunction', 'rtevar', 'instanceof', 'head', 'charsetutf8', 'httpequivcontenttype', 'var', 'vc3', 'styledisplaynone', 'reference', 'ie', 'classnojs', 'langenus', 'endif', 'oldie', 'lgwfull', 'classinlineblock', 'mdblock', 
'classcffooteritem', 'smblock', 'wwwscienceorg', 'ebookscambridgeorg', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'reference', 'jscreadingcompanionreferencesitemp', 'amp', 'dlacmorg', 'hrefjavascript', 'linkref', 'linkreveal', 'classxreflink'
'classcitationlinkscompatibilityspan', 'classname', 'classopeninanotherwindow', 'classlink', 'citationauthorj', 'citationauthord', 'citationjournaltitlechem', 'citationauthors', 'citationauthorm', 'r', 'j', 'classsitemenuitem', 
 '23case', 'efunction', '11case', '15case', '100n', 'keyup', 'keydown', '0case', 'nullfunction', 'display', 'xploremetanav', 'n', '\U00100078\U00100003']

all_stopwords.extend(newStopWords)







# Create your views here.

def index(request):
    return render(request, 'main/index.html')

def home(request):
    results = publications.objects.all()[:100]
    annotation = annotations.objects.all()
    publication_keys = pubkeys.objects.all()

    #most searched keywords
    searched_keywords = records_search.objects.raw('SELECT id, keyword, count(*) as count FROM records_search GROUP BY keyword ORDER BY count DESC LIMIT 5')

    #most opened pubs
    opened_pubs = records_view_publication.objects.raw('SELECT id, pub_title, count(*) as count FROM records_view_publication GROUP BY pub_title ORDER BY count DESC LIMIT 5')

    #most viewed tags
    viewed_tags = records_view_tag.objects.raw('SELECT id, tag, count(*) as count FROM records_view_tag GROUP BY tag ORDER BY count DESC LIMIT 5')

    #most bookmarked
    bookmarked_pubs = records_bookmark.objects.raw('SELECT id, pub_title, count(*) as count FROM records_bookmark GROUP BY pub_title ORDER BY count DESC LIMIT 5')

    #random for author list
    authors_present = []
    authors_tally = []
    authors_single = []
    authors_single_tally = []
    
    for pub in results:
        authors_present.append(pub.author)

    for author in authors_present:
        splitauth = author.split(";") 
        for x in splitauth:
            authors_single.append(x)

    for pub in results:
        authors_tally.append(pub.author)

    for author in authors_tally:
        splitauth = author.split("; ") 
        for x in splitauth:
            authors_single_tally.append(x)

    unique_author = [] #All authors unique

    for auth in authors_single_tally:
        if auth not in unique_author:
            unique_author.append(auth)

    authors = []

    if(unique_author):
        authors= random.choices(unique_author, k=5)

    return render(request, 'main/home.html',{'searched':searched_keywords,'opened_pubs':opened_pubs, 'viewed_tags':viewed_tags,'bookmarked_pubs':bookmarked_pubs,'authors':authors})

def aboutPage(request):
    return render(request, 'main/about.html')

def viewBookmarks(request):
    email = request.session['email']
  
    bookmark = bookmarks.objects.filter(email=email).values('publicationID')
    publication = publications.objects.filter(id__in=bookmark)

    

    return render(request, 'bookmarks.html', {'publications':publication})

#Creates a user account and stores it in the database
def registerView(request):
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.getlist('adriclablist[]'):
            finaladriclist = ','.join(request.POST.getlist('adriclablist[]'))
            saverecord = registerUser()
            saverecord.username = request.POST.get('username')
            if registerUser.objects.filter(username=request.POST.get('username')).exists():
                messages.error(request, 'Sorry. This username is taken', extra_tags='name')
                return redirect('register')
            saverecord.email = request.POST.get('email')
            if registerUser.objects.filter(email=request.POST.get('email')).exists():
                messages.error(request, 'Email already has an account', extra_tags='name')
                return redirect('register')
            saverecord.password = make_password(salt='mySalt',password=request.POST.get('password'))
            if request.POST.get('password') != request.POST.get('repwd'):
                messages.error(request, 'Error: Password does not match', extra_tags='name')
                return redirect('register')
            if  len(str(request.POST.get('password'))) < 8 or request.POST.get('password').islower():
                messages.error(request, 'Error: Password must have at least 8 characters and 1 uppercase letter', extra_tags='name')
                return redirect('register')
            saverecord.first_name = request.POST.get('first_name')
            saverecord.last_name = request.POST.get('last_name')
            saverecord.is_superuser = 0
            saverecord.last_login = time.strftime('%Y-%m-%d %H:%M:%S')
            saverecord.google_scholar_link = request.POST.get('gscholar')
            saverecord.role = finaladriclist
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
        passwordhash = make_password(salt='mySalt',password=request.POST.get('password'))
        try:
            Userdetails=registerUser.objects.get(email=request.POST['email'],password=passwordhash)
            if Userdetails.is_superuser == 1:
                request.session['email']=Userdetails.email
                request.session['username']=Userdetails.username
                request.session['is_superuser']=Userdetails.is_superuser
                return redirect('centerReports')
            else:
                request.session['email']=Userdetails.email
                request.session['username']=Userdetails.username
                request.session['is_superuser']=Userdetails.is_superuser
                if "Student" not in Userdetails.role:
                    return redirect('/profile/' + Userdetails.last_name + ',%20' + Userdetails.first_name)
                else:
                    return redirect('home')
        except registerUser.DoesNotExist as e:
            messages.error(request,'Username or Password Invalid.' , extra_tags='name')
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
    headers = requests.utils.default_headers()

    headers.update(
        {
            'User-Agent': 'user_agent'
        }
    )
   
    flag=False
    print(url)
    source_code=''
    try:
        source_code = requests.get(url,headers=headers).text
        flag= True
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        flag = False
        pass
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
        flag = False
        pass
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
        flag = False
        pass
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
        flag = False
        pass
    except Exception as e:
        print('there is an error,',e)
        flag = False
        pass

    if flag:
        # BeautifulSoup object which will 
        # ping the requested url for data 
        soup = BeautifulSoup(source_code, 'html.parser') 
    
        # Text in given web-page is stored under 
        # the <div> tags with class <entry-content> 

        if "aisel" in url:
            print(id)
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

                    filtered = [word for word in newkeywords if not word in all_stopwords]
                    filtered_dupes = []
                    marker = set()

                    for i in filtered:
                        ll = i.lower()
                        if ll not in marker:
                            marker.add(ll)
                            filtered_dupes.append(i)

                    for i in range(0,len(filtered_dupes)):
                        if keywords.objects.filter(keywordname=filtered_dupes[i].strip()):
                            name_id.append(filtered_dupes[i].strip())
                        else:
                            insert_list.append(keywords(keywordname=filtered_dupes[i].strip()))
                            name_id.append(filtered_dupes[i].strip())

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
        
        if 'doi' in url:
            wordlist = []
            source_code = requests.get(url,headers=headers).text

            # BeautifulSoup object which will
            # ping the requested url for data
            soup = BeautifulSoup(source_code, 'html.parser')
            for each_text in soup.findAll('div'):  
                content = each_text.text
        
            # Text in given web-page is stored under
            # the <div> tags with class <entry-content>
            words = str(source_code).lower().split() 
                            
            for each_word in words: 
                wordlist.append(each_word) 
            clean_wordlist(wordlist, id)

                
        
def clean_wordlist(wordlist, id): 
      
    clean_list =[] 
    for word in wordlist: 
        symbols = '!@#$%^&*()_-+={[}]|;:"<>?/.,\- '
          
        for i in range (0, len(symbols)): 
            word = word.replace(symbols[i], '') 
              
        if len(word) > 0 and len(word) < 60: 
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

    filtered = [word for word in newkeywords if not word in all_stopwords]

    print(filtered)
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

def centerReports(request):
    center_pubs = publications.objects.filter(Q(source__icontains="CAR") | Q(source__icontains="COMET") | Q(source__icontains="CITE4D") |Q(source__icontains="CeLT") |Q(source__icontains="CeHCI") |Q(source__icontains="CNIS") |Q(source__icontains="GameLab") |Q(source__icontains="TE3D House") |Q(source__icontains="Bioinformatics Lab") )

    car_pubs = publications.objects.filter(source__icontains="CAR", status='Approved')
    comet_pubs = publications.objects.filter(source__icontains="COMET", status='Approved')
    cite4d_pubs = publications.objects.filter(source__icontains="CITE4D", status='Approved')
    celt_pubs = publications.objects.filter(source__icontains="CeLT", status='Approved')
    cehci_pubs = publications.objects.filter(source__icontains="CeHCI", status='Approved')
    cnis_pubs = publications.objects.filter(source__icontains="CNIS", status='Approved')
    gamelab_pubs = publications.objects.filter(source__icontains="GameLab", status='Approved')
    te3d_pubs = publications.objects.filter(source__icontains="TE3D House", status='Approved')
    bio_pubs = publications.objects.filter(source__icontains="Bioinformatics Lab", status='Approved')

    return render(request, 'centerReport.html',{'pubs':center_pubs, 
                                                'car':car_pubs, 'car_count':car_pubs.count(),
                                                'comet':comet_pubs, 'comet_count':comet_pubs.count(),
                                                'cite4d':cite4d_pubs, 'cite4d_count':cite4d_pubs.count(),
                                                'celt':celt_pubs, 'celt_count':celt_pubs.count(),
                                                'cehci':cehci_pubs, 'cehci_count':cehci_pubs.count(),
                                                'cnis':cnis_pubs, 'cnis_count':cnis_pubs.count(),
                                                'gamelab':gamelab_pubs, 'gamelab_count':gamelab_pubs.count(),
                                                'te3d':te3d_pubs, 'te3d_count':te3d_pubs.count(),
                                                'bio':bio_pubs, 'bio_count':bio_pubs.count()})

def userProfile(request, user):
    author = user
    if author != None:
        Userdetails=registerUser.objects.get(email=request.session['email'])

        scholarLink = ""

        try:
            scholarLink = Userdetails.google_scholar_link
        except:
            print("Missing field")

        roles = (Userdetails.role).split(',')


        publications_by_author = publications.objects.filter(author__icontains=author)

        pubs = []

        for pub in publications_by_author:
            pubs.append(pub)

        #Make authors into array... from A. author; B. author to ['A. author','B. author']
        for pub in pubs:
            if pub.source == 'IEEE':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            elif pub.source == 'AIS':
                authors = pub.author
                split = authors.split(';')
                pub.author = split
            elif pub.source == 'Scopus':
                authors = []
                authors.append(pub.author)
                pub.author = authors
            elif pub.source == 'Uploaded':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            else:
                authors = pub.author
                split = authors.split('; ')
                pub.author = split

        #clean authors array
        for pub in pubs:
            if pub.source == 'AIS':
                for auth in pub.author:
                    if auth == "":
                        pub.author.remove(auth)

        filteredPubs = []
        test_counter = 0

        #Filtering pubs to find exact author
        for pub in pubs:
            for auth in pub.author:
                if (auth.lower()).strip() == (author.lower()).strip():
                    test_counter+=1
                    filteredPubs.append(pub)

        #Tallying keywords
        sources_present = []
        sources_tally = []
        source_arr = []

        for pub in filteredPubs:
            if pub.source not in sources_present:
                sources_present.append(pub.source)

        for pub in filteredPubs:
            sources_tally.append(pub.source)

        count = 0
        for source in sources_present:
            source_arr.insert(count, [source,sources_tally.count(source)])
            count+=1

        pubkeys_list = list(pubkeys.objects.all())
        keywords_list = list(keywords.objects.all())
        keyword_results = []

        for publication in filteredPubs:
            for pubkey in pubkeys_list:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubkey.status != "pending addition":
                                keyword_results.append(pubid.keywordname)

        keyword_count = Counter(keyword_results).most_common(len(keyword_results))

        filteredPubs.sort(key=lambda x: x.year,reverse=True)

        #Start author recos
        author_recos = []

        #getauthorlast name
        txt = author

        if "." in txt:
            split = txt.split()
            last_name = split[-1]
        elif "," in txt:
            split = txt.replace(',',"")
            split2 = split.split()
            last_name = split2[0]
        else:
            split = txt.split()
            last_name = split[-1]

        author_search = last_name
        results = publications.objects.all()
        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        
        for pub in results:
            authors_present.append(pub.author)

        for txt in authors_present:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single.append(x)

        for pub in results:
            authors_tally.append(pub.author)

        for txt in authors_tally:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single_tally.append(x)

        unique_author = []

        for auth in authors_single_tally:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort()

        author_results = []

        from difflib import SequenceMatcher

        for txt in unique_author:
            if fnmatch.fnmatch(txt, '* '+author_search) or fnmatch.fnmatch(txt, author_search+',*'):
                s_1 = author_search
                s_2 = txt
                if (SequenceMatcher(a=s_1,b=s_2).ratio() > 0.60) and (SequenceMatcher(a=s_1,b=s_2).ratio() != 1):
                    author_results.append(txt)

        count = len(author_results)

        return render(request, 'authorProfile.html',{'author':author.strip(), 'publications':filteredPubs, 'source_arr':source_arr, 'keyword_bar':keyword_count[:10],'query': publications_by_author,'array':pubs,'testC':test_counter,'recos':author_results[:10],'scholarLink':scholarLink,'roles':roles,})


def authorAnalytics(request, author):
    if author != None:
        publications_by_author = publications.objects.filter(author__icontains=author)

        pubs = []

        for pub in publications_by_author:
            pubs.append(pub)

        #Make authors into array... from A. author; B. author to ['A. author','B. author']
        for pub in pubs:
            if pub.source == 'IEEE':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            elif pub.source == 'AIS':
                authors = pub.author
                split = authors.split(';')
                pub.author = split
            elif pub.source == 'Scopus':
                authors = []
                authors.append(pub.author)
                pub.author = authors
            elif pub.source == 'Uploaded':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            else:
                authors = pub.author
                split = authors.split('; ')
                pub.author = split

        #clean authors array
        for pub in pubs:
            if pub.source == 'AIS':
                for auth in pub.author:
                    if auth == "":
                        pub.author.remove(auth)
            


        filteredPubs = []
        test_counter = 0

        #Filtering pubs to find exact author
        for pub in pubs:
            for auth in pub.author:
                if (auth.lower()).strip() == (author.lower()).strip():
                    test_counter+=1
                    filteredPubs.append(pub)

        #Tallying keywords
        sources_present = []
        sources_tally = []
        source_arr = []

        for pub in filteredPubs:
            if pub.source not in sources_present:
                sources_present.append(pub.source)

        for pub in filteredPubs:
            sources_tally.append(pub.source)

        count = 0
        for source in sources_present:
            source_arr.insert(count, [source,sources_tally.count(source)])
            count+=1

        pubkeys_list = list(pubkeys.objects.all())
        keywords_list = list(keywords.objects.all())
        keyword_results = []

        for publication in filteredPubs:
            for pubkey in pubkeys_list:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubkey.status != "pending addition":
                                keyword_results.append(pubid.keywordname)

        keyword_count = Counter(keyword_results).most_common(len(keyword_results))

        filteredPubs.sort(key=lambda x: x.year,reverse=True)

        #Start author recos
        author_recos = []

        #getauthorlast name
        txt = author

        if "." in txt:
            split = txt.split()
            last_name = split[-1]
        elif "," in txt:
            split = txt.replace(',',"")
            split2 = split.split()
            last_name = split2[0]
        else:
            split = txt.split()
            last_name = split[-1]

        author_search = last_name
        results = publications.objects.all()
        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        
        for pub in results:
            authors_present.append(pub.author)

        for txt in authors_present:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single.append(x)

        for pub in results:
            authors_tally.append(pub.author)

        for txt in authors_tally:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single_tally.append(x)

        unique_author = []

        for auth in authors_single_tally:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort()

        author_results = []

        # for txt in unique_author:
        #     if fnmatch.fnmatch(txt, '* '+author_search) or fnmatch.fnmatch(txt, author_search+',*'):
        #         author_results.append(txt)

        # from difflib import SequenceMatcher
        # for txt in unique_author:
        #     s_1 = author_search
        #     s_2 = txt
        #     if (SequenceMatcher(a=s_1,b=s_2).ratio() > 0.60) and (SequenceMatcher(a=s_1,b=s_2).ratio() != 1):
        #         author_results.append(txt)

        from difflib import SequenceMatcher

        for txt in unique_author:
            if fnmatch.fnmatch(txt, '* '+author_search) or fnmatch.fnmatch(txt, author_search+',*'):
                s_1 = author_search
                s_2 = txt
                if (SequenceMatcher(a=s_1,b=s_2).ratio() > 0.60) and (SequenceMatcher(a=s_1,b=s_2).ratio() != 1):
                    author_results.append(txt)

        count = len(author_results)

        return render(request, 'authorAnalytics.html',{'author':author.strip(), 'publications':filteredPubs, 'source_arr':source_arr, 'keyword_bar':keyword_count[:10],'query': publications_by_author,'array':pubs,'testC':test_counter,'recos':author_results[:10]})

def authorAnalyticsFilterKeyword(request, author, keyword):
    if author != None:
        publications_by_author = publications.objects.filter(author__icontains=author)
        keywords_list = list(keywords.objects.all())
        pubkeys_list = list(pubkeys.objects.all())

        pubs = []

        for pub in publications_by_author:
            pubs.append(pub)

        #Make authors into array... from A. author; B. author to ['A. author','B. author']
        for pub in pubs:
            if pub.source == 'IEEE':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            elif pub.source == 'AIS':
                authors = pub.author
                split = authors.split(';')
                pub.author = split
            elif pub.source == 'Scopus':
                authors = []
                authors.append(pub.author)
                pub.author = authors
            elif pub.source == 'Uploaded':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            else:
                authors = pub.author
                split = authors.split('; ')
                pub.author = split

        #clean authors array
        for pub in pubs:
            if pub.source == 'AIS':
                for author in pub.author:
                    if author == "":
                        pub.author.remove(author)

        filteredPubs = []
        test_counter = 0

        #Filtering pubs to find exact author
        for pub in pubs:
            for auth in pub.author:
                if (auth.lower()).strip() == (author.lower()).strip():
                    test_counter+=1
                    filteredPubs.append(pub)

        keywordFilteredPubs = []
        resultsId_list = []

        for keywordL in keywords_list:
            if keyword.lower() == keywordL.keywordname.lower():
                resultsId_list.append(keywordL.id)

        for resultsid in resultsId_list:
            for pubid in pubkeys_list:
                if resultsid == pubid.keywords_id:
                    for pub in filteredPubs:
                        if pubid.publication_id == pub.id:
                            keywordFilteredPubs.append(pub)

        #Tallying keywords
        sources_present = []
        sources_tally = []
        source_arr = []

        for pub in keywordFilteredPubs:
            if pub.source not in sources_present:
                sources_present.append(pub.source)

        for pub in keywordFilteredPubs:
            sources_tally.append(pub.source)

        count = 0
        for source in sources_present:
            source_arr.insert(count, [source,sources_tally.count(source)])
            count+=1

        keyword_results = []

        for publication in keywordFilteredPubs:
            for pubkey in pubkeys_list:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubkey.status != "pending addition":
                                keyword_results.append(pubid.keywordname)

        keyword_count = Counter(keyword_results).most_common(len(keyword_results))

        keywordFilteredPubs.sort(key=lambda x: x.year,reverse=True)

        #Start author recos
        author_recos = []

        #getauthorlast name
        txt = author

        if "." in txt:
            split = txt.split()
            last_name = split[-1]
        elif "," in txt:
            split = txt.replace(',',"")
            split2 = split.split()
            last_name = split2[0]

        author_search = last_name
        results = publications.objects.all()
        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        
        for pub in results:
            authors_present.append(pub.author)

        for txt in authors_present:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single.append(x)

        for pub in results:
            authors_tally.append(pub.author)

        for txt in authors_tally:
            splitauth = txt.split(";") 
            for x in splitauth:
                authors_single_tally.append(x)

        unique_author = []

        for auth in authors_single_tally:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort()

        author_results = []

        # for txt in unique_author:
        #     if fnmatch.fnmatch(txt, '* '+author_search) or fnmatch.fnmatch(txt, author_search+',*'):
        #         author_results.append(txt)

        # from difflib import SequenceMatcher
        # for txt in unique_author:
        #     s_1 = author_search
        #     s_2 = txt
        #     if (SequenceMatcher(a=s_1,b=s_2).ratio() > 0.60) and (SequenceMatcher(a=s_1,b=s_2).ratio() != 1):
        #         author_results.append(txt)

        from difflib import SequenceMatcher

        for txt in unique_author:
            if fnmatch.fnmatch(txt, '* '+author_search) or fnmatch.fnmatch(txt, author_search+',*'):
                s_1 = author_search
                s_2 = txt
                if (SequenceMatcher(a=s_1,b=s_2).ratio() > 0.60) and (SequenceMatcher(a=s_1,b=s_2).ratio() != 1):
                    author_results.append(txt)

        count = len(author_results)

        return render(request, 'authorAnalyticsFilterKeyword.html',{'author':author.strip(), 'publications':keywordFilteredPubs, 'source_arr':source_arr, 'keyword_bar':keyword_count[:10],'keywordFilter':keyword,'recos':author_results[:10]})


def analytics(request, keyword):
    #most searched keywords
    searched_keywords = records_search.objects.raw('SELECT id, keyword, count(*) as count FROM records_search GROUP BY keyword ORDER BY count DESC LIMIT 10')

    #most opened pubs
    opened_pubs = records_view_publication.objects.raw('SELECT id, pub_title, count(*) as count FROM records_view_publication GROUP BY pub_title ORDER BY count DESC LIMIT 10')

    #most viewed tags
    viewed_tags = records_view_tag.objects.raw('SELECT id, tag, count(*) as count FROM records_view_tag GROUP BY tag ORDER BY count DESC LIMIT 10')

    #most bookmarked
    bookmarked_pubs = records_bookmark.objects.raw('SELECT id, pub_title, count(*) as count FROM records_bookmark GROUP BY pub_title ORDER BY count DESC LIMIT 10')

    keyword_search = keyword

    if keyword_search != None:

        if (request.user):
            author = request.session['username']
        else:
            author="null"

        email = request.session['email']

        searched = keyword_search
        searchFilter = "default"
        results_list = []
        resultsId_list = []
        pubkeys_list = list(pubkeys.objects.all())
        keywords_list = list(keywords.objects.all())
        publications_list = list(publications.objects.all())

        my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
        my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

        for keyword in keywords_list:
            if keyword_search.lower() == keyword.keywordname.lower():
                resultsId_list.append(keyword.id)

        for resultsid in resultsId_list:
            for pubid in pubkeys_list:
                if resultsid == pubid.keywords_id:
                    for pub in publications_list:
                        if pubid.publication_id == pub.id:
                            results_list.append(pub)

        keyword_results = []
        author_results = []

        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        author_arr = []
        
        for pub in results_list:
            if pub.author not in authors_present:
                authors_present.append(pub.author)

        for author in authors_present:
            splitauth = [x.strip() for x in author.split(';')]
            for x in splitauth:
                if x:
                    authors_single.append(x)

        for pub in results_list:
            authors_tally.append(pub.author)

        for author in authors_tally:
            splitauth = [x.strip() for x in author.split(';')]
            for x in splitauth:
                if x:
                    authors_single_tally.append(x)

        count = 0
        for author in authors_single:
            author_arr.insert(count, [author,authors_single_tally.count(author)])
            count+=1
        
        unique_author = []

        for auth in author_arr:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort(key=lambda s:s[1], reverse=True)

        years_present = []
        years_tally = []
        year_arr = []   

        for pub in results_list:
            if int(pub.year) not in years_present:
                years_present.append(int(pub.year))

        years_present.sort()

        for pub in results_list:
            years_tally.append(int(pub.year))

        years_tally.sort()

        count = 0
        for year in years_present:
            year_arr.insert(count, [year,years_tally.count(year)])
            count+=1


        sources_present = []
        sources_tally = []
        source_arr = []

        for pub in results_list:
            if pub.source not in sources_present:
                sources_present.append(pub.source)

        for pub in results_list:
            sources_tally.append(pub.source)

        count = 0
        for source in sources_present:
            source_arr.insert(count, [source,sources_tally.count(source)])
            count+=1
    

        for publication in results_list:
            for pubkey in pubkeys_list:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubkey.status != "pending addition":
                                keyword_results.append(pubid.keywordname)
        
        filteredYear =[]
        for year in results_list:
            if int(year.year) not in filteredYear:
                filteredYear.append(int(year.year))

        filteredYear.sort()
        
        print(results_list)

        keyword_count = Counter(keyword_results).most_common(len(keyword_results))
        print(keyword_count)

        #Make authors into array... from A. author; B. author to ['A. author','B. author']
        for pub in results_list:
            if pub.source == 'IEEE':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            elif pub.source == 'AIS':
                authors = pub.author
                split = authors.split(';')
                pub.author = split
            elif pub.source == 'Scopus':
                authors = []
                authors.append(pub.author)
                pub.author = authors
            elif pub.source == 'Uploaded':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            else:
                authors = pub.author
                split = authors.split('; ')
                pub.author = split

        #clean authors array
        for pub in results_list:
            if pub.source == 'AIS':
                for author in pub.author:
                    if author == "":
                        pub.author.remove(author)

        results_list.sort(key=lambda x: x.year,reverse=True)
        
        return render(request, 'testanalytics.html',{'searched':searched.capitalize(), 
                                                    'results':results_list, 
                                                    'count':len(results_list),
                                                    'keyword_results':keyword_count,
                                                    'keyword_bar':keyword_count[:10],
                                                    'searchedkeys':searched_keywords,
                                                    'opened_pubs':opened_pubs, 
                                                    'viewed_tags':viewed_tags,
                                                    'bookmarked_pubs':bookmarked_pubs,
                                                    'year_arr':year_arr[-5:],
                                                    'source_arr':source_arr,
                                                    'author_arr':unique_author[:10]
                                                    })

    return render(request, 'testanalytics.html',{'searchedkey':searched_keywords,'opened_pubs':opened_pubs, 'viewed_tags':viewed_tags,'bookmarked_pubs':bookmarked_pubs})

def analyticsFilterKeyword(request, keyword, keyword2):
    #most searched keywords
    searched_keywords = records_search.objects.raw('SELECT id, keyword, count(*) as count FROM records_search GROUP BY keyword ORDER BY count DESC LIMIT 10')

    #most opened pubs
    opened_pubs = records_view_publication.objects.raw('SELECT id, pub_title, count(*) as count FROM records_view_publication GROUP BY pub_title ORDER BY count DESC LIMIT 10')

    #most viewed tags
    viewed_tags = records_view_tag.objects.raw('SELECT id, tag, count(*) as count FROM records_view_tag GROUP BY tag ORDER BY count DESC LIMIT 10')

    #most bookmarked
    bookmarked_pubs = records_bookmark.objects.raw('SELECT id, pub_title, count(*) as count FROM records_bookmark GROUP BY pub_title ORDER BY count DESC LIMIT 10')

    keyword_search = keyword
    keyword_search2 = keyword2

    if keyword_search != None:

        if (request.user):
            author = request.session['username']
            
        else:
            author="null"

        email = request.session['email']
        searched = keyword_search
        searched2 = keyword_search2
        searchFilter = "default"
        results_list_old = []
        resultsId_list_old = []
        pubkeys_list = list(pubkeys.objects.all())
        keywords_list = list(keywords.objects.all())
        publications_list = list(publications.objects.all())

        my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
        my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

        for keyword in keywords_list:
            if keyword_search.lower() == keyword.keywordname.lower():
                resultsId_list_old.append(keyword.id)

        for resultsid in resultsId_list_old:
            for pubid in pubkeys_list:
                if resultsid == pubid.keywords_id:
                    for pub in publications_list:
                        if pubid.publication_id == pub.id:
                            results_list_old.append(pub)

        results_list = []
        resultsId_list = []

        for keyword in keywords_list:
            if keyword_search2.lower() == keyword.keywordname.lower():
                resultsId_list.append(keyword.id)

        for resultsid in resultsId_list:
            for pubid in pubkeys_list:
                if resultsid == pubid.keywords_id:
                    for pub in results_list_old:
                        if pubid.publication_id == pub.id:
                            results_list.append(pub) 

        keyword_results = []
        author_results = []

        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        author_arr = []
        
        for pub in results_list:
            if pub.author not in authors_present:
                authors_present.append(pub.author)

        for author in authors_present:
            splitauth = [x.strip() for x in author.split(';')]
            for x in splitauth:
                if x:
                    authors_single.append(x)

        for pub in results_list:
            authors_tally.append(pub.author)

        for author in authors_tally:
            splitauth = [x.strip() for x in author.split(';')]
            for x in splitauth:
                if x:
                    authors_single_tally.append(x)

        count = 0
        for author in authors_single:
            author_arr.insert(count, [author,authors_single_tally.count(author)])
            count+=1
        
        unique_author = []

        for auth in author_arr:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort(key=lambda s:s[1], reverse=True)

        years_present = []
        years_tally = []
        year_arr = []   

        for pub in results_list:
            if int(pub.year) not in years_present:
                years_present.append(int(pub.year))

        years_present.sort()

        for pub in results_list:
            years_tally.append(int(pub.year))

        years_tally.sort()

        count = 0
        for year in years_present:
            year_arr.insert(count, [year,years_tally.count(year)])
            count+=1


        sources_present = []
        sources_tally = []
        source_arr = []

        for pub in results_list:
            if pub.source not in sources_present:
                sources_present.append(pub.source)

        for pub in results_list:
            sources_tally.append(pub.source)

        count = 0
        for source in sources_present:
            source_arr.insert(count, [source,sources_tally.count(source)])
            count+=1
    

        for publication in results_list:
            for pubkey in pubkeys_list:
                if publication.id == pubkey.publication_id:
                    for pubid in keywords_list:
                        if pubkey.keywords_id == pubid.id:
                            if pubkey.status != "pending addition":
                                keyword_results.append(pubid.keywordname)
        
        filteredYear =[]
        for year in results_list:
            if int(year.year) not in filteredYear:
                filteredYear.append(int(year.year))

        filteredYear.sort()
        
        print(results_list)

        keyword_count = Counter(keyword_results).most_common(len(keyword_results))
        print(keyword_count)

        #Make authors into array... from A. author; B. author to ['A. author','B. author']
        for pub in results_list:
            if pub.source == 'IEEE':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            elif pub.source == 'AIS':
                authors = pub.author
                split = authors.split(';')
                pub.author = split
            elif pub.source == 'Scopus':
                authors = []
                authors.append(pub.author)
                pub.author = authors
            elif pub.source == 'Uploaded':
                authors = pub.author
                split = authors.split('; ')
                pub.author = split
            else:
                authors = pub.author
                split = authors.split('; ')
                pub.author = split

        #clean authors array
        for pub in results_list:
            if pub.source == 'AIS':
                for author in pub.author:
                    if author == "":
                        pub.author.remove(author)

        results_list.sort(key=lambda x: x.year,reverse=True)
        
        return render(request, 'testanalytics.html',{'searched':searched.capitalize(), 'searched2':searched2.capitalize(),
                                                    'results':results_list, 
                                                    'count':len(results_list),
                                                    'keyword_results':keyword_count,
                                                    'keyword_bar':keyword_count[:10],
                                                    'searchedkeys':searched_keywords,
                                                    'opened_pubs':opened_pubs, 
                                                    'viewed_tags':viewed_tags,
                                                    'bookmarked_pubs':bookmarked_pubs,
                                                    'year_arr':year_arr[-5:],
                                                    'source_arr':source_arr,
                                                    'author_arr':unique_author[:10]
                                                    })

    return render(request, 'testanalytics.html',{'searchedkey':searched_keywords,'opened_pubs':opened_pubs, 'viewed_tags':viewed_tags,'bookmarked_pubs':bookmarked_pubs})



# def countYearResults(year, word):

#     count = publications.objects.filter(year=year, title__icontains=word).count()
#     print(count)
#     return(count)

def searchKeywordAnalytics(request):
    if request.method == "GET":
        keyword_search = request.GET.get("searchedKeyword")
        keyword_results = keywords.objects.filter(keywordname__icontains=keyword_search).order_by('keywordname')
        count = keyword_results.count()

        return render(request, 'main/searchKeywordAnalytics.html',{ 'keyword_results':keyword_results, 'searched': keyword_search, 'count':count})

def searchAuthorAnalytics(request):
    if request.method == "GET":
        
        author_search = request.GET.get("searchedAuthor")
        results = publications.objects.all()
        authors_present = []
        authors_tally = []
        authors_single = []
        authors_single_tally = []
        
        for pub in results:
            authors_present.append(pub.author)

        for author in authors_present:
            splitauth = author.split(";") 
            for x in splitauth:
                authors_single.append(x)

        for pub in results:
            authors_tally.append(pub.author)

        for author in authors_tally:
            splitauth = author.split(";") 
            for x in splitauth:
                authors_single_tally.append(x)

        authors_stripped = []
        
        for author in authors_single_tally:
            lstrip_auth = author.lstrip()
            if lstrip_auth not in authors_stripped:
                authors_stripped.append (lstrip_auth)

        unique_author = []

        for auth in authors_stripped:
            if auth not in unique_author:
                unique_author.append(auth)

        unique_author.sort()

        author_results = []

        for author in unique_author:
            if author_search.lower() in str(author).lower():
                author_results.append(author)

        count = len(author_results)

        return render(request, 'main/searchAuthorAnalytics.html',{ 'author_results':author_results, 'searched': author_search, 'count':count})


def searchPublication(request):
    
    if request.method == "GET":
        
        # searched = request.POST['searched']
        # searchFilter = request.POST['filterData']
        
        # libFilter = request.POST.getlist('filterLib')

        keyword_search = request.GET.get('keyword')
        print(keyword_search)
        if keyword_search != None:

            libFilter = request.GET.getlist('filterLib')
            
            if len(libFilter) > 0: 
                if "[" in libFilter[0]:
                    
                    temp = libFilter[0]
                    libFilter = []
                    print(temp)
                    libFilter.append(temp.strip("['']"))

            if (request.user):
                author = request.session['username']
            else:
                author="null"

            email = request.session['email']

            searched = keyword_search
            searchFilter = "default"
            results_list = []
            resultsId_list = []
            pubkeys_list = list(pubkeys.objects.all())
            keywords_list = list(keywords.objects.all())
            publications_list = list(publications.objects.all())

            my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
            my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

            for keyword in keywords_list:
                if keyword_search == keyword.keywordname:
                    resultsId_list.append(keyword.id)

            for resultsid in resultsId_list:
                for pubid in pubkeys_list:
                    if resultsid == pubid.keywords_id:
                        for pub in publications_list:
                            if pubid.publication_id == pub.id:
                                results_list.append(pub)

            keyword_results = []
            keyword_count = []
            
            
            for publication in results_list:
                for pubkey in pubkeys_list:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)
                                    
            url = str(request.get_full_path())
            if 'ais' in url and 'scopus' in url and 'ieee' in libFilter:
                libFilter = 'default'
                request.session['libFilter'] = "default"
                
            filteredYear =[]
            for year in results_list:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()
            
            

            #Log view tag
            datenow = datetime.datetime.now()

            #check if visited within the day
            check_visit = records_view_tag.objects.filter(user=email, tag=keyword_search, date=datenow)

            if not check_visit:
                logTag = records_view_tag()
                logTag.user = email
                logTag.tag = keyword_search
                logTag.date = datenow
                logTag.save()
            
            if request.GET.get('sortBy') != None:
                if request.GET.get('sortBy') == 'earlyYear':
                    results_list = sorted(results_list, key=lambda publications: publications.year)
                    results_list = results_list.order_by('year')
                elif request.GET.get('sortBy') == 'lateYear':
                    results_list = sorted(results_list, key=lambda publications: publications.year)
                    results_list = results_list.order_by('-year')
            
            if request.GET.get('min') != None and request.GET.get('max') != None:
                min_value = request.GET.get('min')
                max_value = request.GET.get('max')
                results_list = results_list.filter(year__gte=min_value,year__lte=max_value)

            paginator = Paginator(results_list, 20)
            page = request.GET.get('page')

            try:
                results_list = paginator.page(page)
            except PageNotAnInteger:
                results_list = paginator.page(1)  
            except EmptyPage:
                results_list = paginator.page(paginator.num_pages)

            index = len(results_list)-1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            page_range = paginator.page_range[start_index:end_index]

            

            
            return render(request, 'main/search.html',{'searched':searched, 
                                                        'results':results_list, 
                                                        'count':len(results_list),
                                                        'page_range': page_range,
                                                        'keyword_results':keyword_results, 
                                                        'bookmarks': my_bookmarks_folder_contents, 
                                                        'my_bookmarks_id': my_bookmarks_folder, 
                                                        'filteredYear': filteredYear,
                                                        'searchFilter': searchFilter,
                                                        'libFilter':libFilter
                                                        })

        year_search = request.GET.get('year')
        if year_search != None:

            libFilter = request.GET.getlist('filterLib')

            if len(libFilter) > 0: 
                if "[" in libFilter[0]:
                    print("i am in if statement")
                    temp = libFilter[0]
                    libFilter = []
                    print(temp)
                    libFilter.append(temp.strip("['']"))

            if (request.user):
                author = request.session['username']
            else:
                author="null"

            email = request.session['email']

            searched = request.GET.get('searched')
            searchFilter = "default"
            results_list = []
            resultsId_list = []
            pubkeys_list = list(pubkeys.objects.all())
            keywords_list = list(keywords.objects.all())
            publications_list = list(publications.objects.all())

            my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
            my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents

            
            for keyword in keywords_list:
                if keyword_search == keyword.keywordname or searched == keyword.keywordname:
                    resultsId_list.append(keyword.id)

            for resultsid in resultsId_list:
                for pubid in pubkeys_list:
                    if resultsid == pubid.keywords_id:
                        for pub in publications_list:
                            if pubid.publication_id == pub.id and pub.year == year_search:
                                results_list.append(pub)


            # if len(results_list) == 0:
            #     results_list = publications.objects.filter(
            #             Q(title__icontains=searched, year =year_search)  |
            #             Q(author__icontains=searched, year =year_search), status__icontains="approved"
                        
            #     )
                        

            keyword_results = []
            year_count = []

            url = str(request.get_full_path())
            if 'ais' in url and 'scopus' in url and 'ieee' in libFilter:
                libFilter = 'default'
                request.session['libFilter'] = "default"

            for publication in results_list:
                for pubkey in pubkeys_list:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)
            
            filteredYear =[]
            for year in results_list:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))
                    # year_count.append(countResults(year.year))

            filteredYear.sort()
            
            zippedList = zip(filteredYear, year_count)

            paginator = Paginator(results_list, 20)
            page = request.GET.get('page')

            try:
                results_list = paginator.page(page)
            except PageNotAnInteger:
                results_list = paginator.page(1)  
            except EmptyPage:
                results_list = paginator.page(paginator.num_pages)

            index = len(results_list)-1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            page_range = paginator.page_range[start_index:end_index]

            
            
            
            return render(request, 'main/search.html',{'searched':searched, 
                                                        'results':results_list, 
                                                        'count':len(results_list),
                                                        'page_range': page_range,
                                                        'keyword_results':keyword_results, 
                                                        'bookmarks': my_bookmarks_folder_contents, 
                                                        'my_bookmarks_id': my_bookmarks_folder, 
                                                        'filteredYear': filteredYear,
                                                        'searchFilter': searchFilter,
                                                        'libFilter':libFilter
                                                        })


        searched = request.GET.get('searched','')
        searchFilter = request.GET.get('filterData','')
        libFilter = request.GET.getlist('filterLib')
        yearSort = request.GET.get('sortBy', '')
        
        
        url = str(request.get_full_path())
      

        # if request.session['newSearch'] == 0:
        #     request.session['newSearch'] == 0


        if 'ais' in url and 'scopus' in url and 'ieee' in libFilter:
            libFilter = 'default'
            request.session['libFilter'] = "default"
            

        if (request.user):
            author = request.session['username']
        else:
            author="null"

        email = request.session['email']

        my_bookmarks_folder = bookmarks_folder.objects.filter(user=email, folder_name='My Bookmarks').values('id') #get my bookmarks folderID
        my_bookmarks_folder_contents = bookmarks.objects.filter(user=email, folderID__in=my_bookmarks_folder).values('publicationID') #get my bookmarks contents


        results_list = []
        resultsId_list = []
        pubkeys_list = list(pubkeys.objects.all())
        keywords_list = list(keywords.objects.all())
        publications_list = list(publications.objects.all())

        # if len(libFilter) > 0: 
        #     if "[" in libFilter[0]:
        #         print("i am in if statement")
        #         temp = libFilter[0]
        #         libFilter = []
        #         print(temp)
        #         libFilter.append(temp.strip("['']"))
        
        if len(libFilter) > 0: 
            if "[" in libFilter[0]:
                 temp = str(libFilter).replace('[','').replace(']','').replace('\'','').replace('\"','')
                
                 temp2 = temp.replace(", ", ",")
                 print(temp2)
                 libFilter = []
                 libFilter = temp2.split(",")

        
        if  searchFilter == "default":

        

            if 'ais' in libFilter and len(libFilter) == 1:


                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains='ais', status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and pub.source == "ais":
                                    results_list.append(pub)
             


            elif 'ais' in libFilter and 'ieee' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains='ais') |
                    Q(source__icontains='ieee')
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and (pub.source == "ais" or pub.source == "iee"):
                                    results_list.append(pub)


            elif 'ais' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ais") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and (pub.source == "ais" or pub.source == "scopus"):
                                    results_list.append(pub)

             

            elif 'ieee' in libFilter and len(libFilter) == 1:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="ieee", status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and (pub.source == "iee"):
                                    results_list.append(pub)

               

                
            elif 'ieee' in libFilter and 'scopus' in libFilter and len(libFilter) == 2:
                results = publications.objects.filter(
                    Q(source__icontains="ieee") |
                    Q(source__icontains="scopus")
                ).filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and (pub.source == "iee" or pub.source == "scopus"):
                                    results_list.append(pub)

               
            elif 'scopus' in libFilter and len(libFilter) == 1:

                print("hi im searching by scopus only")
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), source__icontains="scopus", status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id and (pub.source == "scopus"):
                                    results_list.append(pub)

              

            else:
                results = publications.objects.filter(
                    Q(title__icontains=searched) |
                    Q(author__icontains=searched), status__icontains="approved"
                ).order_by('id')

                for keyword in keywords_list:
                    if keyword_search == keyword.keywordname:
                        resultsId_list.append(keyword.id)

                for resultsid in resultsId_list:
                    for pubid in pubkeys_list:
                        if resultsid == pubid.keywords_id:
                            for pub in publications_list:
                                if pubid.publication_id == pub.id:
                                    results_list.append(pub)

            

        
            #final list of publications
            final_list = []
            


            in_results_list = set(results_list)
            in_results = set(results)

            in_results_but_not_in_first = in_results - in_results_list

            final_list = results_list + list(in_results_but_not_in_first)

            final_list_ids = [pub.id for pub in final_list]

            results = publications.objects.filter(pk__in=final_list_ids)

            results.order_by('id')
            

            # publication results in list data type                        
            xlist =     list(results)
            for publication in xlist:
                if publication.url == 'doi.org/' or len(publication.url) == 0:
                    publication.url = 'https://scholar.google.com/scholar?q=' + publication.title
                    publication.save()

            publication_keys = pubkeys.objects.all()
            keywords_list = keywords.objects.all()
            keyword_results = []
            year_count = []
            publications_all = publications.objects.all()

            # for publication in list(publications_all):
            #     for result in xlist:
            #         if result.id != publication.id:     
            #             for pubid in list(publication_keys):
            #                 if publication.id == pubid.publication_id:
            #                     for keyword in list(keywords_list):
            #                         if searched == keyword.keywordname:
            #                             xlist.append(publication)


           
            
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

            for publication in results:
                if publication.source != 'Uploaded':
                    for pubkey in publication_keys:
                        if publication.id == pubkey.publication_id:
                            flag = 1
            
            for publication in results:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)
                                    
                                    
            
            


            filteredYear =[]
            for year in results:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))
                    

            filteredYear.sort()
            # for year in filteredYear:
            #     year_count.append(countResults(year,searched))

            zippedList = zip(year_count,filteredYear)
            #Log Search
            logSearch = records_search()
            logSearch.user = email
            logSearch.keyword = searched
            logSearch.filter = searchFilter
            
            if not libFilter:
                source = "['ais', 'ieee', 'scopus']"
            else:
                source = libFilter
            
            

            if request.GET.get('sortBy') != None:
                if request.GET.get('sortBy') == 'earlyYear':
                    results = results.order_by('year')
                    libFilter = str(libFilter).replace('[','').replace(']','').replace('\'','').replace('\"','')
                elif request.GET.get('sortBy') == 'lateYear':
                    results = results.order_by('-year')
                    libFilter = str(libFilter).replace('[','').replace(']','').replace('\'','').replace('\"','')
            
            if request.GET.get('min') != None and request.GET.get('max') != None:
                min_value = request.GET.get('min')
                max_value = request.GET.get('max')
                results = results.filter(year__gte=min_value,year__lte=max_value)
                results = results.order_by('year')
                libFilter = str(libFilter).replace('[','').replace(']','').replace('\'','').replace('\"','')

            result_count = results.count()

            logSearch.source = source
            logSearch.num_results = result_count
            logSearch.date = datetime.datetime.now()
            logSearch.save()
                              
            paginator = Paginator(results, 20)
            page = request.GET.get('page')

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)  
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            index = results.number - 1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            page_range = paginator.page_range[start_index:end_index]

            
            

            return render(request,'main/search.html',{'searched':searched, 
                                                        'results':results, 
                                                        'page_range': page_range,
                                                        'count':result_count,
                                                        'keyword_results':keyword_results, 
                                                        'bookmarks': my_bookmarks_folder_contents, 
                                                        'my_bookmarks_id': my_bookmarks_folder, 
                                                        'filteredYear': filteredYear,
                                                        'searchFilter': searchFilter,
                                                        'libFilter':libFilter,
                                                        })
            
        elif searchFilter == "title":

            if len(libFilter) > 0: 
                if "[" in libFilter[0]:
                    print("i am in if statement")
                    temp = libFilter[0]
                    libFilter = []
                    print(temp)
                    libFilter.append(temp.strip("['']"))
            
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

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname)


            filteredYear =[]
            for year in xlist:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()

            #Log Search
            logSearch = records_search()
            logSearch.user = email
            logSearch.keyword = searched
            logSearch.filter = searchFilter

            if not libFilter:
                source = "['ais', 'ieee', 'scopus']"
            else:
                source = libFilter

            


            if request.GET.get('sortBy') != None:
                if request.GET.get('sortBy') == 'earlyYear':
                    results = results.order_by('year')
                elif request.GET.get('sortBy') == 'lateYear':
                    results = results.order_by('-year')

            if request.GET.get('min') != None and request.GET.get('max') != None:
                min_value = request.GET.get('min')
                max_value = request.GET.get('max')
                results = results.filter(year__gte=min_value,year__lte=max_value)
                results = results.order_by('year')


            logSearch.source = libFilter
            logSearch.num_results = results.count()
            logSearch.date = datetime.datetime.now()
            logSearch.save()

            paginator = Paginator(results, 20)
            page = request.GET.get('page')
            result_count = results.count()

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)  
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            

            index = results.number-1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            page_range = paginator.page_range[start_index:end_index]

            
           

            print("im at title != none")
            return render(request, 'main/search.html',{'searched':searched, 
                                                        'results':results, 
                                                        'count':result_count,
                                                        'keyword_results':keyword_results, 
                                                        'bookmarks': my_bookmarks_folder_contents, 
                                                        'my_bookmarks_id': my_bookmarks_folder, 
                                                        'filteredYear': filteredYear,
                                                        'searchFilter': searchFilter,
                                                        'libFilter':libFilter})

        elif searchFilter == "author":

            if len(libFilter) > 0: 
                if "[" in libFilter[0]:
                    print("i am in if statement")
                    temp = libFilter[0]
                    libFilter = []
                    print(temp)
                    libFilter.append(temp.strip("['']"))

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

            for publication in xlist:
                for pubkey in publication_keys:
                    if publication.id == pubkey.publication_id:
                        for pubid in keywords_list:
                            if pubkey.keywords_id == pubid.id:
                                if pubid.keywordname not in keyword_results:
                                    keyword_results.append(pubid.keywordname) 


            filteredYear =[]
            for year in xlist:
                if int(year.year) not in filteredYear:
                    filteredYear.append(int(year.year))

            filteredYear.sort()

            if not libFilter:
                source = "['ais', 'ieee', 'scopus']"
            else:
                source = libFilter

            #Log Search
            logSearch = records_search()
            logSearch.user = email
            logSearch.keyword = searched
            logSearch.filter = searchFilter

            if not libFilter:
                source = "['ais', 'ieee', 'scopus']"
            else:
                source = libFilter

            

            if request.GET.get('sortBy') != None:
                if request.GET.get('sortBy') == 'earlyYear':
                    results = results.order_by('year')
                elif request.GET.get('sortBy') == 'lateYear':
                    results = results.order_by('-year')
            
            
            if request.GET.get('min') != None and request.GET.get('max') != None:
                min_value = request.GET.get('min')
                max_value = request.GET.get('max')
                results = results.filter(year__gte=min_value,year__lte=max_value)
                results = results.order_by('year')

            results_count = results.count()

            logSearch.source = libFilter
            logSearch.num_results = results.count()
            logSearch.date = datetime.datetime.now()
            logSearch.save()


            paginator = Paginator(results, 20)
            page = request.GET.get('page')

            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)  
            except EmptyPage:
                results = paginator.page(paginator.num_pages)

            index = results.number-1
            max_index = len(paginator.page_range)
            start_index = index - 5 if index >= 5 else 0
            end_index = index + 5 if index <= max_index - 5 else max_index
            page_range = paginator.page_range[start_index:end_index]

            
            
            print("im at author != none")
            return render(request, 'main/search.html',{'searched':searched, 
                                                       'results':results, 
                                                       'count':results_count,
                                                       'keyword_results':keyword_results, 
                                                       'bookmarks': my_bookmarks_folder_contents, 
                                                       'my_bookmarks_id': my_bookmarks_folder, 
                                                       'filteredYear': filteredYear,
                                                       'searchFilter': searchFilter,
                                                       'libFilter':libFilter})
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

            # for publication in xlist:
            #         flag = 0
            #         for pubkey in publication_keys:
            #             if publication.id == pubkey.publication_id and flag == 0:
            #                 flag=1
            #         if flag == 0:
            #             if "http" in publication.url: 
            #                 scrap(publication.url, publication.id)
            #             else:
            #                 scrap("http://" + publication.url, publication.id)

            
            if request.GET.get('sortBy') != None:
                if request.GET.get('sortBy') == 'earlyYear':
                    results = results.order_by('year')
                elif request.GET.get('sortBy') == 'lateYear':
                    results = results.order_by('-year')
            
            if request.GET.get('min') != None and request.GET.get('max') != None:
                min_value = request.GET.get('min')
                max_value = request.GET.get('max')
                results = results.filter(year__gte=min_value,year__lte=max_value)
                results = results.order_by('year')

            

            return render(request, 'main/search.html',{ 'keyword_results':keyword_results})





def removeKeywordRequest(request, id, keyword):

    email = request.session['email']
    next = request.POST.get('next', '/')

    keyword_ids = pubkeys.objects.all()
    keywords_list = keywords.objects.all()

    
    xlist = list(keyword_ids)

    if request.method == 'POST':
        print(id)
        for pubid in xlist:
            if int(id) == int(pubid.publication_id):
                print(pubid.publication_id)
                print(pubid.keywords_id)
                keywordname = keywords.objects.get(id = pubid.keywords_id)
                print(keywordname.keywordname)
                if keyword == keywordname.keywordname:
                    print(pubid.id)
                    edit_pubkey = pubkeys.objects.get(id=pubid.id)
                    edit_pubkey.status= "pending deletion"
                    edit_pubkey.save()
        messages.success(request, "Request for keyword deletion sent")
        return HttpResponseRedirect(next)  
    else:
        return HttpResponseRedirect(next)


def addKeywordRequest(request, id):

    email = request.session['email']
    next = request.POST.get('next', '/')
    previous = request.POST.get('previous')
    
    

    if request.method == 'POST':
        
        insert_list = []
        name_id = []
        pub_id = []
        status = []
        key_id = request.POST.get('addedKeyword').split(",")
        for i in range(0,len(key_id)):
            if keywords.objects.filter(keywordname=key_id[i].strip()):
                name_id.append(key_id[i].strip())
                
            else:
                insert_list.append(keywords(keywordname=key_id[i].strip()))
                name_id.append(key_id[i].strip())
                

        keywords.objects.bulk_create(insert_list)
        
        for j in range(0,len(name_id)):
            store = keywords.objects.get(keywordname=name_id[j])
            pub_id.append(pubkeys(publication_id=id, keywords_id=store.id, status = "pending addition"))
            
        pubkeys.objects.bulk_create(pub_id)
        messages.success(request, "Request for keyword addition sent")
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(request.META['HTTP_REFERER'])


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

def SearchAnnotationFolder(request,username):
    email = request.session['email']
    searched = request.GET.get('searched')

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

    annotates = annotations.objects.filter(folderID__in=folders.values('id'),body__icontains=searched)
    sharedAnnotates = annotations.objects.filter(folderID__in=shared_folders_ids,body__icontains=searched)


    return render(request, 'main/folders-search.html',{'bookmarks':bookmark,
                                                    'folders':folders,
                                                    'rawbookmarks':rawbookmarks,
                                                    'collaborators':collaborator,
                                                    'collabs':collabs,
                                                    'sharedfolders': shared_folders,
                                                    'sharedbookmarks': shared_folders_bookmarks,
                                                    'sharedpubs':shared_folders_pubs,
                                                    'searched':searched,
                                                    'annotations':annotates,
                                                    'sharedAnnotations':sharedAnnotates,})

def FoldersPageAnalytics(request, folderID):
    email = request.session['email']
    folder = bookmarks_folder.objects.filter(id=folderID)
    folderpubs = bookmarks.objects.filter(user=email,folderID=folderID).values('publicationID')
    pubs = publications.objects.filter(id__in=folderpubs)

    ais_authors = pubs.filter(source='AIS').values('author')
    iee_authors = pubs.filter(source='IEEE').values('author')
    scopus_authors = pubs.filter(source='Scopus').values('author')

    all_authors = []

    # for author in ais_authors:
    #     print(author)
    #     for item in author.split(';'):
    #         all_authors.append(item)

    # for author in iee_authors:
    #     for item in author.split(';'):
    #         all_authors.append(item)

    # for author in scopus_authors:
    #     all_authors.append(author)

    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()
    keyword_results = []
    
    xlist = list(pubs)

    for publication in xlist:
        for pubkey in publication_keys:
            if publication.id == pubkey.publication_id:
                for pubid in keywords_list:
                    if pubkey.keywords_id == pubid.id:
                        if pubkey.status != "pending addition":
                            keyword_results.append(pubid.keywordname)


    resultsId_list = []

    for keyword in keyword_results:
        for allkeys in keywords_list:
            if keyword == allkeys.keywordname:
                resultsId_list.append(allkeys.id)

    keyword_count = Counter(keyword_results).most_common(len(keyword_results))

    pubkeys_list = list(pubkeys.objects.all())
    publications_list = list(publications.objects.all())
    relatedPubs = []

    for resultsid in resultsId_list:
        for pubid in pubkeys_list:
            if resultsid == pubid.keywords_id:
                for pub in publications_list:
                    if pubid.publication_id == pub.id and pub not in pubs:
                        relatedPubs.append(pub)

    years_present = []  
    years_tally = []
    year_arr = []
            

    for pub in xlist:
        if int(pub.year) not in years_present:
            years_present.append(int(pub.year))

    years_present.sort()

    for pub in xlist:
        years_tally.append(int(pub.year))

    years_tally.sort()

    count = 0
    for year in years_present:
        year_arr.insert(count, [year,years_tally.count(year)])
        count+=1

    sources_present = []
    sources_tally = []
    source_arr = []

    for pub in xlist:
        if pub.source not in sources_present:
            sources_present.append(pub.source)

    for pub in xlist:
        sources_tally.append(pub.source)

    count = 0
    for source in sources_present:
        source_arr.insert(count, [source,sources_tally.count(source)])
        count+=1

    authors_present = []
    authors_tally = []
    authors_single = []
    authors_single_tally = []
    author_arr = []
    
    for pub in pubs:
        if pub.author not in authors_present:
            authors_present.append(pub.author)

    for author in authors_present:
        splitauth = [x.strip() for x in author.split(';')]
        for x in splitauth:
            if x:
                authors_single.append(x)

    for pub in pubs:
        authors_tally.append(pub.author)

    for author in authors_tally:
        splitauth = [x.strip() for x in author.split(';')]
        for x in splitauth:
            if x:
                authors_single_tally.append(x)

    count = 0
    for author in authors_single:
        author_arr.insert(count, [author,authors_single_tally.count(author)])
        count+=1
    
    unique_author = []

    for auth in author_arr:
        if auth not in unique_author:
            unique_author.append(auth)

    unique_author.sort(key=lambda s:s[1], reverse=True)

    if not pubs:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #Make authors into array... from A. author; B. author to ['A. author','B. author']
    for pub in pubs:
        if pub.source == 'IEEE':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        elif pub.source == 'AIS':
            authors = pub.author
            split = authors.split(';')
            pub.author = split
        elif pub.source == 'Scopus':
            authors = []
            authors.append(pub.author)
            pub.author = authors
        elif pub.source == 'Uploaded':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        else:
            authors = pub.author
            split = authors.split('; ')
            pub.author = split

    #clean authors array
    for pub in pubs:
        if pub.source == 'AIS':
            for author in pub.author:
                if author == "":
                    pub.author.remove(author)

    return render(request, 'testfolderanalytics.html',{'folder':folder,
                                                       'results':pubs,
                                                       'related':relatedPubs, 
                                                       'keyword_results': keyword_count,
                                                       'keyword_bar': keyword_count[:10],
                                                       'year_arr':year_arr[-5:],
                                                       'source_arr':source_arr,
                                                       'ais':ais_authors,
                                                       'ieee':iee_authors,
                                                       'scopus':scopus_authors,
                                                       'all':all_authors,
                                                       'author_arr':unique_author[:10],
                                                       'searched':folder,
                                                       })

def SharedFoldersPageAnalytics(request, folderID, owner):
    folder = bookmarks_folder.objects.filter(id=folderID)
    folderpubs = bookmarks.objects.filter(user=owner,folderID=folderID).values('publicationID')
    pubs = publications.objects.filter(id__in=folderpubs)

    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()
    keyword_results = []
    xlist = list(pubs)

    for publication in xlist:
        for pubkey in publication_keys:
            if publication.id == pubkey.publication_id:
                for pubid in keywords_list:
                    if pubkey.keywords_id == pubid.id:
                        if pubkey.status != "pending addition":
                            keyword_results.append(pubid.keywordname)

    resultsId_list = []

    for keyword in keyword_results:
        for allkeys in keywords_list:
            if keyword == allkeys.keywordname:
                resultsId_list.append(allkeys.id)

    
    keyword_count = Counter(keyword_results).most_common(len(keyword_results))


    pubkeys_list = list(pubkeys.objects.all())
    publications_list = list(publications.objects.all())
    relatedPubs = []

    for resultsid in resultsId_list:
        for pubid in pubkeys_list:
            if resultsid == pubid.keywords_id:
                for pub in publications_list:
                    if pubid.publication_id == pub.id and pub not in pubs:
                        relatedPubs.append(pub)

    years_present = []  
    years_tally = []
    year_arr = []
            

    for pub in xlist:
        if int(pub.year) not in years_present:
            years_present.append(int(pub.year))

    years_present.sort()

    for pub in xlist:
        years_tally.append(int(pub.year))

    years_tally.sort()

    count = 0
    for year in years_present:
        year_arr.insert(count, [year,years_tally.count(year)])
        count+=1

    sources_present = []
    sources_tally = []
    source_arr = []

    for pub in xlist:
        if pub.source not in sources_present:
            sources_present.append(pub.source)

    for pub in xlist:
        sources_tally.append(pub.source)

    count = 0
    for source in sources_present:
        source_arr.insert(count, [source,sources_tally.count(source)])
        count+=1

    authors_present = []
    authors_tally = []
    authors_single = []
    authors_single_tally = []
    author_arr = []
    
    for pub in pubs:
        if pub.author not in authors_present:
            authors_present.append(pub.author)

    for author in authors_present:
        splitauth = [x.strip() for x in author.split(';')]
        for x in splitauth:
            if x:
                authors_single.append(x)

    for pub in pubs:
        authors_tally.append(pub.author)

    for author in authors_tally:
        splitauth = [x.strip() for x in author.split(';')]
        for x in splitauth:
            if x:
                authors_single_tally.append(x)

    count = 0
    for author in authors_single:
        author_arr.insert(count, [author,authors_single_tally.count(author)])
        count+=1
    
    unique_author = []

    for auth in author_arr:
        if auth not in unique_author:
            unique_author.append(auth)

    unique_author.sort(key=lambda s:s[1], reverse=True)

    if not pubs:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    #Make authors into array... from A. author; B. author to ['A. author','B. author']
    for pub in pubs:
        if pub.source == 'IEEE':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        elif pub.source == 'AIS':
            authors = pub.author
            split = authors.split(';')
            pub.author = split
        elif pub.source == 'Scopus':
            authors = []
            authors.append(pub.author)
            pub.author = authors
        elif pub.source == 'Uploaded':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        else:
            authors = pub.author
            split = authors.split('; ')
            pub.author = split

    #clean authors array
    for pub in pubs:
        if pub.source == 'AIS':
            for author in pub.author:
                if author == "":
                    pub.author.remove(author)
                            
    return render(request, 'testfolderanalytics.html',{'folder':folder,
                                                       'results':pubs, 
                                                       'related':relatedPubs,
                                                       'keyword_results': keyword_count,
                                                       'keyword_bar':keyword_count[:10],
                                                       'year_arr':year_arr[-5:],
                                                       'source_arr':source_arr,
                                                       'author_arr':unique_author[:10],
                                                       'searched':folder,
                                                       })

#this function displays the details of a publication that has been selected from the home page
def PublicationPage(request, id):
    results = publications.objects.filter(id=id)
    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()
    keyword_results = []
    keyword_count = []
    xlist = list(results)
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


    #Log opening of publication
    datenow = datetime.datetime.now()

    #check if visited within the day
    check_visit = records_view_publication.objects.filter(user=email, pub_id=id, date=datenow)

    if not check_visit:
        logView = records_view_publication()
        logView.user = email
        for pub in results:
            logView.pub_title = pub.title
        logView.pub_id = id
        logView.date = datenow
        logView.save()

    flag = 0

    for publication in xlist:
        if publication.source != 'Uploaded':
            for pubkey in publication_keys:
                if publication.id == pubkey.publication_id:
                    flag = 1
    
    results = publications.objects.filter(id=id)
    publication_keys = pubkeys.objects.all()
    keywords_list = keywords.objects.all()

    for publication in xlist:
        for pubkey in publication_keys:
            if publication.id == pubkey.publication_id:
                for pubid in keywords_list:
                    if pubkey.keywords_id == pubid.id:
                        if pubid.keywordname not in keyword_results and pubkey.status != "pending addition":
                            keyword_results.append(pubid.keywordname)



    previous = request.META.get('HTTP_REFERER')
    
   
    if 'analyticsAuthor' in previous:
        request.session['search_url'] = previous
        current_url = request.session['search_url']
    elif 'search' in previous:
        request.session['search_url'] = previous
        current_url = request.session['search_url']
    elif 'http://ccscloud1.dlsu.edu.ph:11780/home/' == previous:
        request.session['search_url'] = previous
        current_url = request.session['search_url']
    else:
        current_url = previous #request.session['search_url']

    #Make authors into array... from A. author; B. author to ['A. author','B. author']
    for pub in results:
        if pub.source == 'IEEE':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        elif pub.source == 'AIS':
            authors = pub.author
            split = authors.split(';')
            pub.author = split
        elif pub.source == 'Scopus':
            authors = []
            authors.append(pub.author)
            pub.author = authors
        elif pub.source == 'Uploaded':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        else:
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
            
    #clean authors array
    for pub in results:
        if pub.source == 'AIS':
            for author in pub.author:
                if author == "":
                    pub.author.remove(author)




    return render(request, 'publication.html', {'publication':results,
                                                'annotations':annotation,
                                                'keyword_results':keyword_results,
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
                                                'bool_in_bookmark': in_my_bookmarks,
                                                'my_bookmarks_id': my_bookmarks_folder,
                                                'my_bookmarks_content':my_bookmarks_folder_contents,
                                                'path' : current_url
                                                })

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
                        if pubid.keywordname not in keyword_results and pubkey.status != "pending addition":
                            keyword_results.append(pubid.keywordname)

    #Make authors into array... from A. author; B. author to ['A. author','B. author']
    for pub in results:
        if pub.source == 'IEEE':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        elif pub.source == 'AIS':
            authors = pub.author
            split = authors.split(';')
            pub.author = split
        elif pub.source == 'Scopus':
            authors = []
            authors.append(pub.author)
            pub.author = authors
        elif pub.source == 'Uploaded':
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        else:
            authors = pub.author
            split = authors.split('; ')
            pub.author = split
        
    
    #clean authors array
    for pub in results:
        if pub.source == 'AIS':
            for author in pub.author:
                if author == "":
                    pub.author.remove(author)

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
    current_datetime = datetime.datetime.now()
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
    current_datetime = datetime.datetime.now()
    
    
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
    search_url = request.POST.get('previous', '/')

    if request.method=='POST':
        if request.POST.get("bookmark_action") == 'add':
            pubID = id
            addBookmark = bookmarks()
            addBookmark.user = email
            addBookmark.publicationID = pubID
            addBookmark.folderID = request.POST.get('folder_id')
            addBookmark.save()

            #log bookmarking
            logBookmark = records_bookmark()
            logBookmark.user = email
            logBookmark.pub_id = pubID
            for pub in results:
                logBookmark.pub_title = pub.title
            logBookmark.folder_id = request.POST.get('folder_id')
            logBookmark.date = datetime.datetime.now()
            logBookmark.save()

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

            #log bookmarking
            logBookmark = records_bookmark()
            logBookmark.user = email
            logBookmark.pub_id = pubID
            for pub in results:
                logBookmark.pub_title = pub.title
            logBookmark.folder_id = request.POST.get('folder_id')
            logBookmark.date = datetime.datetime.now()
            logBookmark.save()


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

            #log bookmarking
            logBookmark = records_bookmark()
            logBookmark.user = email
            logBookmark.pub_id = pubID
            for pub in results:
                logBookmark.pub_title = pub.title
            logBookmark.folder_id = request.POST.get('folder_id')
            logBookmark.date = datetime.datetime.now()
            logBookmark.save()

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
        messages.success(request, "Succesfully added collaborator")  
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
            auth_user = registerUser.objects.get(email = request.session['email'])
            user_center = auth_user.role


            savepub = publications()
            savepub.title = request.POST.get('title')
            if publications.objects.filter(title=request.POST.get('title')).exists():
                return render(request, 'upload.html', {'some_flag': True})
            savepub.abstract = request.POST.get('abstract')
            savepub.author = request.POST.get('author')
            savepub.pdf = request.FILES.get('document')
            savepub.url = 'Uploaded'
            savepub.status = 'Pending'
            savepub.source = 'Uploaded'
            date = datetime.datetime.now().date()
            savepub.year = date.strftime("%Y")
            savepub.save()

            if user_center != 'Student':
                record = records_center_uploads()
                record.title = request.POST.get('title')
                record.abstract = request.POST.get('abstract')
                record.author = request.POST.get('author')
                record.pdf = request.FILES.get('document')
                record.url = 'Uploaded'
                record.status = 'Pending'
                record.source = 'Uploaded'
                date = datetime.datetime.now().date()
                record.year = date.strftime("%Y")
                record.center = user_center
                record.save()

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
            messages.success(request, "Succesfully Uploaded. Pending Acceptance")
            return render(request, 'upload.html')#render(request, 'registration/login.html')
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

            try:
                centerReport = records_center_uploads.objects.get(title=stat.title)
                centerReport.status = 'Approved'
                centerReport.save()
            except records_center_uploads.DoesNotExist:
                centerReport = None


            
        elif 'Decline' in request.POST.values():
            pair = [key for key in request.POST.keys()][1].split("|")
            #pair will be a list containing x and y
            dec = publications.objects.get(id=pair[0],title=pair[1])
            dec.delete()
            bkmrk = bookmarks.objects.get(publicationID=pair[0])
            bkmrk.delete()

            try:
                centerReport = records_center_uploads.objects.get(title=dec.title)
                centerReport.delete()
            except records_center_uploads.DoesNotExist:
                centerReport = None

    return render(request, 'main/adminpage.html',{'publications':results})

def uploadExtracts(request):
    if request.method == 'POST':
        # publication_resource = PublicationResource()
        dataset = Dataset()
        new_publications = request.FILES['my_file']
        imported_data = dataset.load(new_publications.read(), format='xlsx')
        for data in imported_data:
            value= publications(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
            )
            value.status='approved'
            value.save()
        center_pubs = publications.objects.filter(Q(source__icontains="CAR") | Q(source__icontains="COMET") | Q(source__icontains="CITE4D") |Q(source__icontains="CeLT") |Q(source__icontains="CeHCI") |Q(source__icontains="CNIS") |Q(source__icontains="GameLab") |Q(source__icontains="TE3D House") |Q(source__icontains="Bioinformatics Lab") )

        car_pubs = publications.objects.filter(source__icontains="CAR", status='Approved')
        comet_pubs = publications.objects.filter(source__icontains="COMET", status='Approved')
        cite4d_pubs = publications.objects.filter(source__icontains="CITE4D", status='Approved')
        celt_pubs = publications.objects.filter(source__icontains="CeLT", status='Approved')
        cehci_pubs = publications.objects.filter(source__icontains="CeHCI", status='Approved')
        cnis_pubs = publications.objects.filter(source__icontains="CNIS", status='Approved')
        gamelab_pubs = publications.objects.filter(source__icontains="GameLab", status='Approved')
        te3d_pubs = publications.objects.filter(source__icontains="TE3D House", status='Approved')
        bio_pubs = publications.objects.filter(source__icontains="Bioinformatics Lab", status='Approved')

        return render(request, 'centerReport.html',{'pubs':center_pubs, 
                                                    'car':car_pubs, 'car_count':car_pubs.count(),
                                                    'comet':comet_pubs, 'comet_count':comet_pubs.count(),
                                                    'cite4d':cite4d_pubs, 'cite4d_count':cite4d_pubs.count(),
                                                    'celt':celt_pubs, 'celt_count':celt_pubs.count(),
                                                    'cehci':cehci_pubs, 'cehci_count':cehci_pubs.count(),
                                                    'cnis':cnis_pubs, 'cnis_count':cnis_pubs.count(),
                                                    'gamelab':gamelab_pubs, 'gamelab_count':gamelab_pubs.count(),
                                                    'te3d':te3d_pubs, 'te3d_count':te3d_pubs.count(),
                                                    'bio':bio_pubs, 'bio_count':bio_pubs.count()})

    return render(request, 'main/uploadextracts.html')
    

def keywordRequests(request):


    if request.method == 'POST':
        
        if 'Accept' in request.POST.values():
            pair = [key for key in request.POST.keys()][1].split("|")
            
            if pair[2] == 'add':

                pubkey_edit = pubkeys.objects.get(id = pair[1])
                pubkey_edit.status = ''
                pubkey_edit.save()
            else:

                pubkeys.objects.filter(id=pair[1]).delete()
                keywords.objects.filter(id=pair[0]).delete()

        elif 'Decline' in request.POST.values():
            pair = [key for key in request.POST.keys()][1].split("|")

            if pair[2] == 'add':

                pubkeys.objects.filter(id=pair[1]).delete()
                keywords.objects.filter(id=pair[0]).delete()

            else:

                pubkey_edit = pubkeys.objects.get(id = pair[1])
                pubkey_edit.status = ''
                pubkey_edit.save()



    publications_all = publications.objects.all()
    results = pubkeys.objects.filter(status__startswith="pending")
    words = keywords.objects.all()
    publications_title = []
    publications_url = []
    publications_keyword = []
    keyword_action = []

    results_list = list(results)
    publications_list = list(publications_all)
    words_list = list(words)

    for pubid in results_list:
        for pub in publications_list:
            if pubid.publication_id == pub.id:
                    publications_title.append(pub.title)
                    publications_url.append(pub.url)
    

    for pubid in results_list:
        for word in words_list:
            if pubid.keywords_id == word.id:
                publications_keyword.append(word.keywordname)
                action = (pubid.status).partition(' ')[2]
                if action == 'deletion':
                    keyword_action.append('delete')
                else:
                    keyword_action.append('add')


    zippedList = zip(results_list,publications_title, publications_url,publications_keyword, keyword_action)

    return render(request, 'main/keywordrequests.html',{'zippedlist': zippedList})

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

        ('FONTNAME', (0,1), (4,1), 'Helvetica'),
        ('FONTSIZE', (0,1), (4,1), 12),
        ('FONTSIZE', (0,0), (4,0), 14),
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
        filterpub = bookmarks.objects.filter(folderID=pair[0]).values('publicationID')

        if not filterpub:
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        getpubs = publications.objects.filter(id__in=filterpub)
        from reportlab.platypus.flowables import KeepTogether
        from reportlab.lib.units import mm

        # List of Lists
        buf = io.BytesIO()
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        title_style = styles['Heading1']
        title_style.alignment = TA_CENTER
        title_style.fontSize=16
        title_style.fontName="Helvetica"
        styleN.alignment = TA_LEFT
        styleN.fontSize=10
        styleN.fontName="Helvetica"
        ptext = "This is an example."
        can = canvas.Canvas(buf, pagesize=A4)
        p = Paragraph(ptext, style=styles["Normal"])
        p.wrapOn(can, 50*mm, 50*mm)  # size of 'textbox' for linebreaks etc.
        p.drawOn(can, 0*mm, 0*mm)
        can.save()
        
        data = [
            ['Year','Title', 'Author', 'Link to Article', 'Base Source']
        ]
        yearData = []

        for pub in getpubs:
            data.append([Paragraph(pub.year, style=styleN),Paragraph(pub.title, style=styleN),Paragraph(pub.author, style=styleN),Paragraph(pub.url, style=styleN),Paragraph(pub.source, style=styleN)])
            yearData.append(int(pub.year))
            #data.append([KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN)),KeepTogether(Paragraph(pub.title, styleN))])
            #data.append([Paragraph(pub.title,styles['Normal']),pub.author,'Title','Title','Title','Title'])
        
        pdf = SimpleDocTemplate(
            buf,
            pagesize=A4,
            format=landscape
        )

        aiscounter = 0
        ieeecounter = 0
        scopuscounter = 0
        othercounter = 0

        lab = []

        for pub in getpubs:
            if pub.source == 'AIS':
                aiscounter = aiscounter + 1
            elif pub.source == 'IEEE':
                ieeecounter = ieeecounter + 1
            elif pub.source == 'Scopus':
                scopuscounter = scopuscounter + 1
            else:
                othercounter = othercounter + 1

        if aiscounter > 0:
            lab.append('AIS')

        if ieeecounter > 0:
            lab.append('IEEE')

        if scopuscounter > 0:
            lab.append('Scopus')

        if othercounter > 0:
            lab.append('Others')

        idata = []
        ledata = []

        for x in lab:
            if x == ('AIS'):
                idata.append(aiscounter)
                aisstore = 'AIS - ' + str(aiscounter)
                ledata.append(aisstore)
            elif x == ('IEEE'):
                idata.append(ieeecounter)
                ieeestore = 'IEEE - ' + str(ieeecounter)
                ledata.append(ieeestore)
            elif x == ('Scopus'):
                idata.append(scopuscounter)
                scopusstore = 'Scopus - ' + str(scopuscounter)
                ledata.append(scopusstore)
            else:
                idata.append(othercounter)
                otherstore = 'Others - ' + str(othercounter)
                ledata.append(otherstore)

        from reportlab.lib.validators import Auto
        from reportlab.graphics.charts.piecharts import Pie

        chart = Pie()
        chart.data = idata
        chart.x = 10
        chart.y = 5

        chart.labels = ledata #lab
        chart.sideLabels = True

        chart.slices[0].fillColor = colors.red

        title = String(
            35, 130, #50, 110,
            'Database Source of Articles', 
            fontSize = 16,
            fontName = "Helvetica"
        )	

        legend = Legend()
        legend.x = 200
        legend.y = 80
        legend.alignment = 'right' 	

        legend.colorNamePairs = Auto(obj=chart)

        drawing = Drawing(300, 200)
        drawing.add(title)
        drawing.add(chart)
        drawing.add(legend)

        drawingbar = Drawing(600, 200)
        yearData.sort(key=int)
        numist = []
        for x in Counter(yearData).values():
            numist.append(x)


        ydata = [
            numist
        ]

        bc = VerticalBarChart()
        bc.x = 50
        bc.y = 50
        bc.height = 125
        bc.width = 350
        bc.data = ydata
        bc.barWidth = .3*inch
        bc.groupSpacing = .2 * inch

        bc.valueAxis.valueMin = 0
        bc.valueAxis.valueMax = 25
        bc.valueAxis.valueStep = 5


        bc.strokeColor = colors.black

        bc.categoryAxis.labels.boxAnchor = 'ne'
        bc.categoryAxis.labels.dx = 8
        bc.categoryAxis.labels.dy = -2

        yearcat = []
        yearNew = list(set(yearData))
        yearNew.sort(key=int)
        for x in yearNew:
            yearcat.append(str(x))

        
        bc.categoryAxis.categoryNames = yearcat


        bc.bars[0].fillColor = colors.green
        bc.bars[1].fillColor = colors.lightgreen

        drawingbar.add(bc)


        table = Table(data, colWidths=(20*mm, 40*mm, 40*mm, 45*mm, 35*mm))
        # add style
        style = TableStyle([
            ('BACKGROUND', (0,0), (4,0), colors.green),
            ('TEXTCOLOR',(0,0),(4,0),colors.whitesmoke),

            ('ALIGN',(0,0),(-1,-1),'CENTER'),

            ('VALIGN', (0, 0), (-1, -1), 'TOP'),

            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (1,0), (-1,-1), 12),
            ('FONTSIZE', (0,0), (-1,4), 14),
            ('BOTTOMPADDING', (0,0), (4,0), 15),
            ('BOTTOMPADDING', (0,0), (4,1), 12),
            #('BACKGROUND',(0,1),(-1,-1),colors.beige),
            
        ])
        table.setStyle(style)
        # 2) Alternate backgroud color
        '''
        rowNumb = len(data)
        for i in range(1, rowNumb):
            if i % 2 != 0:
                bc = colors.beige
            else:
                bc = colors.burlywood
            
            ts = TableStyle(
                [('BACKGROUND', (0,i),(-1,i), bc)]
            )
            table.setStyle(ts)
        '''
        # 3) Add borders
        ts = TableStyle(
            [
            #('BOX',(0,0),(-1,-1),1,colors.black),
            #('LINEBEFORE',(2,1),(2,-1),1,colors.black),
            ('LINEABOVE',(0,0),(-1,-4),1,colors.black),
            ('LINEBELOW',(0,0),(-1,-1),1,colors.black),
            #('GRID',(0,0),(-1,-1),1,colors.black),
            ]
        )
        from reportlab.platypus import  Spacer
        table.setStyle(ts)
        elems = []
        elems.append(Paragraph("Summary of Articles For " + pair[1],style=title_style))
        elems.append(Spacer(1,.25*inch))
        elems.append(table)
        #elems.append(Spacer(1,.5*inch))
        #drawing.hAlign = 'CENTER'
        #elems.append(Paragraph("Date Extracted",style=title_style))
        #elems.append(drawingbar)
        #elems.append(drawing)
        #elems.append(d)
        pdf.build(elems)
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename= pair[1] + ' Summary.pdf')

def downloadExtractTemplate(request):
    templatePath = '/main/'
    templateFile = 'Upload-Extract-Template.xslx'


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