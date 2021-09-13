from django.contrib import admin
from .models import Viewer, ViewerMovie, Movie
# Register your models here.

@admin.register(Viewer)
class ViewerAdmin(admin.ModelAdmin):
    list_display = ('id','username','first_name','last_name','dob')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title','year','genre','plot','lang','poster','rating')

@admin.register(ViewerMovie)
class ViewerMovieAdmin(admin.ModelAdmin):
    list_display = ('id','viewer','movie','watched','favourite', 'rating')
