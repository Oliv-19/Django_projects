from django.shortcuts import render, redirect
import requests
import json
from .models import Content, User_Content
from django.db.models import F
from django.http import HttpResponse, JsonResponse
import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from .forms import CustomUserCreationForm, TypesForm, FilterForm, FilterFormTwo, TypesFormTwo
from datetime import datetime
from django.utils.crypto import get_random_string


# Create your views here.
def api_call_felix(search):
    url = f"https://moviesdatabase.p.rapidapi.com/titles/search/title/{search}"

    querystring = {"exact":"false","info":"base_info", "limit":"50"}

    headers = {
        "X-RapidAPI-Key": "306b3eab4cmshfe2bb7966afe897p10cf3ajsnb0f6770d59a4",
        "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    json_data = json.loads(response.text)['results']

    for i in json_data:

        media_id = i['id']
        title = i['titleText']['text']
        typeContent = i['titleType']['id']

        if typeContent == 'tvMovie':
            typeContent = 'movie'
        elif typeContent == 'movie':
            typeContent = typeContent
        elif typeContent == 'tvSeries':
            typeContent = 'serie'
        elif typeContent == 'tvMiniSeries':
            typeContent = 'serie'
        else:
            print('passed')
            continue

        img = i['primaryImage']['url'] if i['primaryImage'] != None else None
        episodes = i['episodes']['episodes']['total'] if i['episodes'] != None else None
        plot = i['plot']['plotText']['plainText'] if i['plot'] != None else None
        year = i['releaseYear']['year'] if i['releaseYear'] != None else None
        author = None
        if Content.objects.filter(content_id = media_id).exists():
            continue
        else:
            newContent = Content.objects.create(content_id = media_id, title = title, poster =img, description = plot, episodes = episodes,author=author, year=year, typeContent=typeContent)
            newContent.save()
            print('saved'+typeContent)

def books_api_call(search):


    book_search= search.replace(' ', '%20')

    books_url =f'https://www.googleapis.com/books/v1/volumes?q={book_search}&key=AIzaSyCn7KHqPSsNnpeYOCoPb4EpKAmmtpmkeWU'


    books_response = requests.get(books_url)

    books_json_data = json.loads(books_response.text)['items']


    global año
    global author1

    for a in books_json_data:


        books_id = a['id']
        titles= a['volumeInfo']['title']
        img = a['volumeInfo']['imageLinks']['thumbnail'] if 'imageLinks' in a['volumeInfo'].keys() else None
        author = a['volumeInfo']['authors'] if 'authors' in a['volumeInfo'].keys() else None
        year = a['volumeInfo']['publishedDate'] if 'publishedDate' in a['volumeInfo'].keys() else None
        plot = a['volumeInfo']['description'] if 'description' in a['volumeInfo'].keys() else None
        episodes = a['volumeInfo']['pageCount'] if 'pageCount' in a['volumeInfo'].keys() else None
        typeContent = 'Book'

        if year == None:
                pass
        else:
            año = int(str(year)[:4])

        if author != None:
            for i in author:
                author1= i.replace("[", '')
                author1= author1.replace("]", '')
                author1= author1.replace('"', '')
                author1= author1.replace("'", '')
            else:
                None


            if Content.objects.filter(content_id = books_id).exists():
                print('pass book')

            else:
                print('saving book')
                newContent = Content.objects.create(content_id = books_id, title = titles, poster =img, description =plot, episodes = episodes,author=author1, year=año, typeContent=typeContent)
                newContent.save()
 

def games_api_call(search):
    games_url = "https://epic-store-games.p.rapidapi.com/onSale"

    games_querystring = {"searchWords":search,"categories":"Games","locale":"us","country":"us"}

    games_headers = {
        "X-RapidAPI-Key": "306b3eab4cmshfe2bb7966afe897p10cf3ajsnb0f6770d59a4",
        "X-RapidAPI-Host": "epic-store-games.p.rapidapi.com"
    }

    games_response = requests.get(games_url, headers=games_headers, params=games_querystring)

    games_json_data = json.loads(games_response.text)
    global año

    for i in games_json_data:

        games_id = i['id']
        title = i['title']
        if title:
            img = i['keyImages'][1]['url'] if i['keyImages'] != None else None
            episodes = None
            plot = i['description'] if i['description'] != None else None
            year = i['pcReleaseDate'] if i['pcReleaseDate'] != None else None
            author = i['publisherName'] if i['publisherName'] != None else None
            typeContent = 'Games'
            if year != None: año = int(str(year)[:4])

            if Content.objects.filter(content_id = games_id).exists():
                print('pass game')
                continue
            else:
                print('saving game')
                newContent = Content.objects.create(content_id = games_id, title = title, poster =img, description = plot, episodes = episodes,author=author, year=año, typeContent=typeContent)
                newContent.save()


is_index = False

not_login= False

def index(request):

    random_movie = random.choice([i for i in Content.objects.filter(typeContent__search='movie').exclude(poster = '').values()])

    random_book =random.choice([i for i in Content.objects.filter(typeContent__search='Book').exclude(poster = '').values()])
    random_game =random.choice([i for i in Content.objects.filter(typeContent__search='Games').exclude(poster = '').values()])


    popular_movies = random.sample([i for i in Content.objects.filter(typeContent='movie' ).exclude(poster = '').values()], k=6)
    popular_series = random.sample([i for i in Content.objects.filter(typeContent='serie').exclude(poster = '').values()], k=6)
    popular_book = random.sample([i for i in Content.objects.filter(typeContent='Book').exclude(poster = '').values()], k=6)

    popular_games = random.sample([i for i in Content.objects.filter(typeContent='Games').exclude(poster = '').values()], k=6)

    is_index = True
    not_login= True

    return render(request, 'index.html',{'not_login':not_login,'is_index':is_index,'random_game':random_game,'random_movie':random_movie,'random_book': random_book, 'popular_book': popular_book,
                                          'popular_movies': popular_movies, 'popular_series': popular_series,'popular_games': popular_games})

def content(request, pk):
    content_object = Content.objects.get(id=pk)
    ids = {'star1': 1 ,'star2':2 ,'star3' :3 ,'star4':4 ,'star5':5}
    not_login= True
    not_saved= False
    authors = []
    if content_object.author != None:
        splited = content_object.author.split(',')
        for i in splited:
            authors.append(i)
    else:
        authors.append(content_object.author)

    current_user = request.user


    stars_id= None
    if User_Content.objects.filter(user_id=current_user.id, content_id = pk).exists():
        stars = User_Content.objects.get(user_id=current_user.id, content_id = pk)
        stars_id = stars.id
        star_rating= stars.rating
        reviewText = stars.review
        not_saved= True
    else:
        not_saved= False
        star_rating = 0
        reviewText = ''


    return render(request, 'content.html', {'not_saved':not_saved,'user_content_id':stars_id,'reviewPH': reviewText,'stars': star_rating,'current_user_id': current_user.id,'ids':ids,'not_login':not_login,'pk': pk, 'content_object':content_object, 'authors':authors})

def userRating(request, user_id, content_id, rating):
    global reviewText


    user = request.user
    content_object = Content.objects.get(id=content_id)


    object_verify=  User_Content.objects.filter(user_id=user_id, content_id=content_id)


    if object_verify.exists():

        object_verify.update(rating=rating)
    else:

        newContent = User_Content.objects.create(user_id= user, content_id= content_object, rating=rating)
        newContent.save()

    if request.method == 'POST':
        reviewText =  request.POST.get('review')

        if object_verify.exists():

            object_verify.update(review= reviewText)
        else:

            newContent = User_Content.objects.create(user_id= user, content_id= content_object, rating=rating, review= reviewText)
            newContent.save()

    return redirect(f'/content/{content_id}')



def search(request):
    if request.method == 'GET':
        not_login= True
        searchs =  request.GET['content']

        typesForm = TypesForm(request.GET)
        typesFormTwo = TypesFormTwo(request.GET)
        filterForm = FilterForm(request.GET)
        types = request.GET.get('sortTypes')
        filter = request.GET.get('sortFilter')
        current_user = request.user

        if searchs:
            try:
                
                books_api_call(searchs)
            except:
                print('without books apis')


            try:
                
                games_api_call(searchs)
            except:
                print('without game apis')


            try:
                
                api_call_felix(searchs)
            except:
                print('without movie apis')

            user_content = User_Content.objects.filter(user_id = current_user).values_list('content_id')
            
            
            idk = user_content.values('content_id')
            idk2 = []
            for i in idk:
                idk2.append(i['content_id'])
            


            content =  Content.objects.filter(title__search=searchs)

            
            if types != None and filter != None:
                content = filters(content, types, filter, 'search')

            if content:
                content_exist= True
                return render(request, 'search.html', { 'content_exist': content_exist, 'typesFormTwo': typesFormTwo,'idk2':idk2,'filterForm':filterForm,'typesForm':typesForm,'not_login':not_login,'search': f'{searchs}', 'datos': content})
            else:
                content_exist= False
                return render(request, 'search.html', {'content_exist': content_exist, 'typesFormTwo': typesFormTwo,'idk2':idk2,'filterForm':filterForm,'typesForm':typesForm,'not_login':not_login,'search': f'{searchs}'})
                
def addNewContent(request):
    if request.method == 'POST':
        title =   request.POST.get('title')
        img =   request.POST.get('img')
        plot =  request.POST.get('plot')
        episodes =  request.POST.get('episodes')
        author =  request.POST.get('author')
        year =  request.POST.get('year')
        contentType = request.POST.get('sortTypesTwo')
        random_content_id = get_random_string(length=32)


        if episodes == '':
            episodes= 0
            
        else:
            episodes= int(episodes)

        if year != '':
             year=int(year)
        else:
            year= None

        if Content.objects.filter(content_id = random_content_id).exists():
            random_content_id = get_random_string(length=32)
            print('already in')
        else:
            newContent = Content.objects.create(content_id = get_random_string(length=32), title = title, poster =img, description = plot, episodes = episodes,author=author, year=year, typeContent=contentType)
            newContent.save()
            print(newContent.id)



            
        #print('saved'+typeContent)

    return redirect(f'content/{newContent.id}')

def add(request):
    current_user = request.user

    if request.method == 'POST':
        conten_pk =  request.POST.get('content_id')
        content_object = Content.objects.get(id=conten_pk)
        print(conten_pk)
        if User_Content.objects.filter(user_id=current_user.id, content_id = conten_pk).exists():
            print('already in')
            
        else:
            newContent = User_Content.objects.create(user_id= current_user, content_id= content_object)
            newContent.save()
            print('new saved')


    return redirect('content/'+conten_pk)

def delete(request):
    user_content_id =  request.GET.get('user_content_id')
    current_user = request.user
    User_Content.objects.filter(id = user_content_id, user_id = current_user).delete()
    return redirect('/biblioteca')

def content_edit(request, pk):

    if request.method == 'POST':
        content_object = Content.objects.filter(id=pk)
        default_img= content_object.values('poster')
        default_episodes= content_object.values('episodes')
        default_year= content_object.values('year')
        default_author= content_object.values('author')
        
        
        img =   request.POST.get('img')
        plot =  request.POST.get('plot')
        episodes =  request.POST.get('episodes')
        author =  request.POST.get('author')
        year =  request.POST.get('year')

        if img == '':
            img = default_img

        if episodes == '':
            episodes = default_episodes

        if year == '':
            year = default_year

        if author =='':
            author = default_author

       
        if content_object.exists():
            content_object.update(poster =img, description = plot, episodes = episodes,author=author, year=year)
            print('updated')

    return redirect(f'/content/{pk}')

def filters(name, type, filter, urlName):

    filtered_content = name

    if type == None:
        type= 'All'

    if type == 'All':
        filtered_content = filtered_content
    else:
        filtered_content =  filtered_content.filter(typeContent__search=type)

    if urlName == 'search' :

        if filter == 'Latest':

            filtered_content = filtered_content.order_by('-year')
            print('latest')
        elif filter == 'Oldest':

            filtered_content = filtered_content.order_by('year')
            print('oldest')


    elif urlName == 'library':

        if filter == 'Latest':

            filtered_content = filtered_content.order_by('-year')
            print('latest')
        elif filter == 'Oldest':

            filtered_content = filtered_content.order_by('year')
            
        elif filter == 'Latest Addition':
            filtered_content = filtered_content.order_by('-user_created_at')
            
        elif filter == 'Oldest Addition':
            filtered_content = filtered_content.order_by('user_created_at')

        elif filter == 'Rating ASC':
            filtered_content = filtered_content.order_by('-user_rating')

        elif filter == 'Rating DESC':
            filtered_content = filtered_content.order_by('user_rating')

    return filtered_content


def filter_author(request, author_name):
    not_login= True
    typesForm = TypesForm(request.GET)
    filterForm = FilterForm(request.GET)
    types = request.GET.get('sortTypes')
    filter = request.GET.get('sortFilter')

    current_user = request.user
    content_exist= True

    author_content =  Content.objects.filter(author__search=author_name)

    user_content = User_Content.objects.filter(user_id = current_user).values_list('content_id')
    idk = user_content.values('content_id')
    idk2 = []
    for i in idk:
        idk2.append(i['content_id'])

   
    
    if types != None and filter != None:
        author_content= filters(author_content, types, filter, 'search')

    return render(request, 'authors.html', {'content_exist': content_exist, 'idk2':idk2,'filterForm':filterForm,'typesForm':typesForm,'not_login':not_login,'search': author_name, 'datos': author_content})



@login_required
def biblioteca(request):
    typesForm = TypesForm(request.GET)
    filterForm = FilterFormTwo(request.GET)


    types = request.GET.get('sortTypes')
    filter = request.GET.get('sortFilterTwo')


    not_login= True

    current_user = request.user
    ids =  User_Content.objects.filter(user_id = current_user.id)
    content = Content.objects.filter(id__in=ids.values('content_id')).annotate(user_created_at=F('user_content__created_at'), user_rating = F('user_content__rating'))
    user_rating_stars= content.values('user_rating')

    if types != None and filter != None:
        content = filters(content, types, filter, 'library')

    return render(request, 'biblioteca.html',{'Stars': user_rating_stars, 'filterForm':filterForm,'typesForm':typesForm,'not_login':not_login,'datos': content,})

def exit(request):
     logout(request)
     return redirect('/')

is_register= False

def register(request):
    is_register= True
    data = {
         'form': CustomUserCreationForm(),
         'register':is_register

    }
    if request.method == 'POST':
         user_creation_form = CustomUserCreationForm(data=request.POST)


         if user_creation_form.is_valid():

            user_creation_form.save()

            user = authenticate(username = user_creation_form.cleaned_data['username'], password = user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('/')

    return render(request, 'registration/register.html', data)

