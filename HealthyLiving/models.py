from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal


# Create your models here.
class Recipe(models.Model):
    Title = models.CharField(max_length=200)
    categories = models.TextField()
    ingredients = models.TextField()
    directions = models.TextField()
    calories = models.IntegerField()
    words = models.TextField()
    course = models.TextField(default="")
    onestarRating = models.IntegerField(default = 0)
    twostarRating = models.IntegerField(default = 0)
    threestarRating = models.IntegerField(default = 0)
    fourstarRating = models.IntegerField(default = 0)
    fivestarRating = models.IntegerField(default = 0)
    totalRatings = models.IntegerField(default = 0)
    avgRating = models.IntegerField(default = 0)

    def __str__(self):
       return self.Title

class RecentlyViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    Date = models.DateField(blank=False, null=True)

    def __str__(self):
       return self.recipeID.Title

    class Meta:
       ordering = ('-Date',)

class Favourites(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeID = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    Date = models.DateField(blank=False, null=True)
    course = models.TextField(default="")


    def __str__(self):
       return self.recipeID.Title

    class Meta:
        ordering = ('-Date',)

class recommended(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipeId = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    date = models.DateField(blank=False, null=True)
