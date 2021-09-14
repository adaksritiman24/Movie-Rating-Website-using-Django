from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Viewer(User):
    dob = models.DateField()

class Movie(models.Model):
    title = models.CharField(max_length=100)
    year = models.CharField(max_length=4)
    genre = models.CharField(max_length= 100)
    plot = models.CharField(max_length=2000)
    lang = models.CharField(max_length=70)
    poster = models.ImageField(upload_to = "posters/", null = True)
    rating = models.DecimalField(decimal_places = 2, null = True, blank = True, max_digits=6)
    

class ViewerMovie(models.Model):
    viewer = models.ForeignKey(Viewer, on_delete= models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete= models.CASCADE)
    watched = models.IntegerField(null = True)
    favourite = models.IntegerField(null = True)
    rating = models.IntegerField(null = True)
    review = models.CharField(max_length=150, null = True)
    rtime = models.DateTimeField(null = True)
