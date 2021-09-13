"""movie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home, name = 'home'),
    path('signup/',views.SignupView.as_view(), name = 'signup'),
    path('login/',views.LoginView.as_view(), name = 'login'),
    path('dashboard/',views.dashboard, name = 'dash'),
    path('logout/',views.logoutuser, name = 'logout'),

    path('watched/<int:viewerid>/',views.watched, name = 'watched'),
    path('favourites/<int:viewerid>/',views.favourites, name = 'favourites'),
    
    path('moviepage/<int:movieid>/<int:viewerid>/',views.moviepage, name = 'moviepage'),
    path('moviepage/<int:movieid>/<int:viewerid>/addtowatchlist/',views.addtowatchlist_fn, name = 'addtowatchlist'),
    path('moviepage/<int:movieid>/<int:viewerid>/removefromwatchlist/',views.removefromwatchlist_fn, name = 'removefromwatchlist'),
    
    path('moviepage/<int:movieid>/<int:viewerid>/addtofavourites/',views.addtofavourites_fn, name = 'addtofavourites'),
    path('moviepage/<int:movieid>/<int:viewerid>/removefromfavourites/',views.removefromfavourites_fn, name = 'removefromfavourites'),

    path('moviepage/<int:movieid>/<int:viewerid>/submitrating/',views.submitrating_fn, name = 'submitrating'),
    path('moviepage/<int:movieid>/<int:viewerid>/removerating/',views.removeRating, name = 'removerating'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
