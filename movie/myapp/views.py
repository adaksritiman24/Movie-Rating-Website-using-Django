from typing import final
from django.conf import settings
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from .forms import ViewerCreationForm, LoginForm
from django.views import View
from .models import Viewer, Movie, ViewerMovie
from django.contrib.auth.forms import AuthenticationForm
from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
import datetime

# Create your views here.

def home(request):
    return render(request,'myapp/home.html')

class SignupView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = ViewerCreationForm()
            return render(request, 'myapp/signup.html',{'form':fm})
        else:
            return redirect('/dashboard/')    
    def post(self, request):
        fm = ViewerCreationForm(request.POST)
        if fm.is_valid():
            fm.save()
            messages.success(request,'Account Created Successfully')    
            fm = ViewerCreationForm()
        else:
            messages.error(request, "Coudn't create USer")    
        return render(request, 'myapp/signup.html',{'form':fm})        

class LoginView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            fm = LoginForm()
            return render(request, 'myapp/login.html',{'form':fm}) 
        else:
            return redirect('/dashboard/') 

    def post(self, request):
        fm = LoginForm(request= request, data = request.POST)
        username = request.POST['username']    
        password = request.POST['password'] 
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success( request, 'Succcessfully logged in !')
            return redirect('/dashboard/')
        else:
            messages.error(request, "Invalid credentials!") 
            return render(request, 'myapp/login.html',{'form':fm})          

def dashboard(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all().order_by('-rating')
        return render(request, "myapp/dashboard.html",{'user':request.user ,  'allmovies':movies})
    else:
        return redirect('/login/')     

def logoutuser(request):
    logout(request)
    return redirect('/')

def moviepage(request,movieid,viewerid):
    if request.user.is_authenticated:
        try:
            vm = ViewerMovie.objects.get(viewer = viewerid, movie = movieid)
        except:
            vm = {
                'watched' : None,
                'favourite': None,
                'rating':None,
            }    
        movie = Movie.objects.get(pk = movieid)
        no_of_ratings = ViewerMovie.objects.filter(movie_id = movieid, rating__isnull = False).count()
        revs = ViewerMovie.objects.select_related('viewer').filter(movie_id = movieid, review__isnull=False).order_by('-rtime')
        top3_reviews = []
        count = 0
        for re in revs:
            count+=1
            top3_reviews.append({'reviewer':re.viewer.username,'review': re.review,'time':re.rtime})
            if count==3:
                break 
        context = {
            'user': request.user,
            'movie':movie,
            'vm': vm,
            'no_of_ratings': no_of_ratings,
            'reviews': top3_reviews,
        }
        return render(request, 'myapp/moviepage.html', context)
    else:
        return redirect('/login/')     

def addtowatchlist_fn(request, movieid, viewerid):
    print('addtowatchlist called')
    movie = movieid
    viewer = viewerid
    
    nor = ViewerMovie.objects.filter(movie = movie, viewer = viewer).update(watched = 1)
    if nor == 0:
        vm =ViewerMovie(movie_id = movie, viewer_id = viewer, watched = 1)
        vm.save()
    return JsonResponse({'success':'Added'})

def removefromwatchlist_fn(request, movieid, viewerid):
    print('removefromwatchlist called')
    movie = movieid
    viewer = viewerid
    
    nor = ViewerMovie.objects.filter(movie = movie, viewer = viewer).update(watched = 0)
    return JsonResponse({'success':'Removed'})

def addtofavourites_fn(request, movieid, viewerid):
    print('addtofavourites called')
    movie = movieid
    viewer = viewerid
    
    nor = ViewerMovie.objects.filter(movie = movie, viewer = viewer).update(favourite = 1)
    if nor == 0:
        vm =ViewerMovie(movie_id = movie, viewer_id = viewer, favourite = 1)
        vm.save()
    return JsonResponse({'success':'Added'})

def removefromfavourites_fn(request, movieid, viewerid):
    print('removefromfavourites called')
    movie = movieid
    viewer = viewerid
    
    nor = ViewerMovie.objects.filter(movie = movie, viewer = viewer).update(favourite = 0)
    return JsonResponse({'success':'Removed'})

@csrf_exempt
def submitrating_fn(request, movieid, viewerid):
    print('submit rating called')
    rat = int(request.POST['rat'])
    nor = ViewerMovie.objects.filter(movie = movieid, viewer = viewerid).update(rating = rat)
    if nor == 0:
        vm =ViewerMovie(movie_id = movieid, viewer_id = viewerid, rating = rat)
        vm.save()
    ratingAvg = ViewerMovie.objects.filter(movie = movieid).aggregate(Avg('rating'))    
    print(ratingAvg)
    Movie.objects.filter(id = movieid).update(rating=ratingAvg['rating__avg'])

    return JsonResponse({'success':'Rated'})

def watched(request, viewerid):
    if request.user.is_authenticated:
        cursor = connection.cursor()
        query = f"select * from myapp_movie where id in (select movie_id from myapp_viewermovie where viewer_id = '{viewerid}' and watched = 1)"
        cursor.execute(query)
        row = cursor.fetchall()
        movies = []
        for item in row:
            id = item[0]
            title = item[1]
            if len(title)>15:
                title = title[:15]+'..'    
            genre = item[3]
            plot = item[4]
            lang = item[5]
            poster = item[6]
            rating = item[7]
            movies.append({'id' : id, 'title':title,'genre':genre, 'plot':plot[:100]+'...','lang':lang, 'poster':poster,'rating':rating})
        return render(request, 'myapp/watched.html',{'watchlist':movies,'userid':viewerid})
    else:
        return redirect('/login/') 

def favourites(request, viewerid):
    if request.user.is_authenticated:
        cursor = connection.cursor()
        query = f"select * from myapp_movie where id in (select movie_id from myapp_viewermovie where viewer_id = '{viewerid}' and favourite = 1)"
        cursor.execute(query)
        row = cursor.fetchall()
        movies = []
        for item in row:
            id = item[0]
            title = item[1]
            if len(title)>15:
                title = title[:15]+'..'    
            genre = item[3]
            plot = item[4]
            lang = item[5]
            poster = item[6]
            rating = item[7]
            movies.append({'id' : id, 'title':title,'genre':genre, 'plot':plot[:100]+'...','lang':lang, 'poster':poster,'rating':rating})
        return render(request, 'myapp/favourite.html', {'favourites':movies,'userid':viewerid})
    else:
        return redirect('/login/')     

def removeRating(request, movieid, viewerid):
    if request.user.is_authenticated:
        nor = ViewerMovie.objects.filter(movie = movieid, viewer = viewerid).update(rating = None)
        ratingAvg = ViewerMovie.objects.filter(movie = movieid).aggregate(Avg('rating'))    
        # print(ratingAvg)
        Movie.objects.filter(id = movieid).update(rating=ratingAvg['rating__avg'])
        return JsonResponse({'success':'Rating Removed'})
    else:
       return redirect('/login/')    
@csrf_exempt
def postReview(request, movieid, viewerid):
    if request.user.is_authenticated:
        review = request.POST['review']
        timenow = datetime.datetime.now()
        nor = ViewerMovie.objects.filter(movie = movieid, viewer = viewerid).update(review=review, rtime = timenow )
        if nor == 0:
            vm =ViewerMovie(movie_id = movieid, viewer_id = viewerid,review=review, rtime = timenow)
            vm.save()  
        return JsonResponse({'time':timenow.strftime('%b. %d, %Y, %I:%M %p'.lstrip('0'))})   
    else:
        return redirect('/login/')    

def deleteReview(request, movieid, viewerid):
    if request.user.is_authenticated:
        nor = ViewerMovie.objects.filter(movie = movieid, viewer = viewerid).update(review=None, rtime = None)

        return JsonResponse({'Success':'Review Deleted'})    
    else:    
        return redirect('/login/')    