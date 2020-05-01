from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.generic import ListView, DetailView
from django.utils.timezone import now
from django.utils.timezone import datetime
from django.core.paginator import Paginator
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import os
import time
from HealthyLivingApp.settings import RECOMMEND_DIR
url = os.path.join(RECOMMEND_DIR, 'MasterRecipeFile.csv')

#Import models
from Users.models import Profile,HealthData
from .models import *
from Users.models import Profile
from .filters import searchFilter
#import python libraries
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# Create your views here.


df = pd.read_csv(url,sep = ',')
df.categories.fillna(' ', inplace=True)
df.isna().sum()
#df.info()
df.set_index('title', inplace = True)

custom  = pd.read_csv(url ,sep = ',')
custom1  = pd.read_csv(url ,sep = ',')
custom.set_index('title', inplace = True)

def recommend(food):

    course = custom.loc[food,'course']
    newtable = custom1[(custom1['course'] == course)]
    array = []
    #Populate the array first with the titles of the recipes.
    for i in newtable['title']:
        array.append(i)

    #Gets the ID of the recipe
    recipeId = array.index(food)
    #Initialise the vector for words
    countVector = CountVectorizer()
    #Create a matrix which contains a vector count for each recipe
    VectorFreq = countVector.fit_transform(newtable['words'])

    #Compute the cosine similarity with the recipe provided against the other recipes in the dataset
    #Prevents the need for computing the entire matrix
    cos_Sim = cosine_similarity(VectorFreq[recipeId], VectorFreq)

    #Creates an array which holds the similarity values for all the recipes
    ls = []
    ls = cos_Sim

    #Create a 2D array which holds a recipe and its corresponding similarity to a recipe recommended
    foodarray = []
    for i in range(len(array)):
        #Add to teh 2D array the recipe id,its title and its corresponding
        #similarity value to the recipe we are comparing to
        foodarray.append([array[i],ls[0][i]])

    #Use functional lamda to order the array by ascending cosine similarity value
    foodarray.sort(key = lambda x:x[1],reverse=True)
    #Only return a sub array of the 10 highest similar recipes
    return foodarray[1:5]

def home(request):
    if not request.user.is_authenticated:
        return render(request,'HealthyLiving/home.html')

    favlist = []
    recentlist = []
    messageFav = ""
    messageRecent = ""
    try:
        #Check to see if the record exists by date to prevent duplicates
        fav = Favourites.objects.filter(user = request.user).latest('id')
        #Get recommendation based of user's recently favourite recipe
        favLs = []
        favRecommend = recommend(fav.recipeID.Title)
        for i in range(len(favRecommend)):
            #print(favRecommend[i][0])
            favLs.append(Recipe.objects.get(Title = favRecommend[i][0]))

        favlist = list(favLs)
        print(favlist)
    except Favourites.DoesNotExist:
        messageFav = "None for favourites"
        print("None for favourites")

    try:
        #Check to see if the record exists by date to prevent duplicates
        recent = RecentlyViewed.objects.filter(user = request.user).latest('Date')
        ls = recommend(recent.recipeID.Title)
        foodLs = []
        foodContext = {}
        #Get recommendation based of user's browsing history
        for i in range(len(ls)):
            #print(ls[i][0])
            foodLs.append(Recipe.objects.get(Title = ls[i][0]))

        recentlist = list(foodLs)
        print(recentlist)
    except RecentlyViewed.DoesNotExist:
        messageRecent = "None for recentlist"
        print("None for recentlist")

    userRatings = Rated.objects.filter(user = request.user)[:5]
    userfav = Favourites.objects.filter(user = request.user)[:5]

    Context = {
        'Recent' : favlist,
        'Favourite' : recentlist,
        'Rated' : list(userRatings),
        'Favorites' : list(userfav),
        'messagefav': messageFav,
        'messagerecent':messageRecent,
    }
    return render(request,'HealthyLiving/home.html',Context)

def search(request):
    recipe_filter = searchFilter(request.GET, queryset=Recipe.objects.all())
    return render(request,'HealthyLiving/search.html', {'filter':recipe_filter,})

def test(request):
    userRatings = Rated.objects.filter(user = request.user)[:4]
    if userRatings.count() == 0:
        ratingExist = "No rated items"
    else:
        ratingExist = list(userRatings)
    print(userRatings.count())
    userfav = Favourites.objects.filter(user = request.user)[:4]
    print(userfav)
    context = {
        'Rated' : list(userRatings),
        'Favorites' : list(userfav),
    }

    subject = 'Subject'
    html_message = render_to_string('HealthyLiving/email-update.html', context)
    plain_message = strip_tags(html_message)
    from_email =  'mohamedtestemail98@gmail.com'
    to = request.user.email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    return render(request,'HealthyLiving/test.html', context)

def searchView1(request):
    return JsonResponse({
        'Items': list( Recipe.objects.values()),
    })

class PostListView(ListView):
    model = Recipe
    template_name = 'HealthyLiving/recipes.html'
    queryset = Recipe.objects.all()
    context_object_name = 'Recipe'
    paginate_by = 9

    def get_queryset(self):
        title = self.request.GET.get('q')
        course = self.request.GET.get('filter')
        print(title)
        print(course)
        if course == None:
            return Recipe.objects.all()

        if title != '':
            if (self.request.GET.get('filter') == 'All'):
                return Recipe.objects.filter(Title__contains=self.request.GET.get('q'))
            else:
                return Recipe.objects.filter(Title__contains=self.request.GET.get('q'),
                 course__contains=self.request.GET.get('filter'))
        else:
            if (self.request.GET.get('filter') == 'All'):
                return Recipe.objects.filter(Title__contains=self.request.GET.get('q'))
            else:
                return Recipe.objects.filter(course__contains=self.request.GET.get('filter'))

class PostDetailView(DetailView):
    model = Recipe

def recentlyVisited(request , pk):
    if not request.user.is_authenticated:
        return JsonResponse({
            'recieved' : 'nope'
        })
    recipe = Recipe.objects.get(pk = request.POST['recipeID'])
    recipeName = recipe.Title
    user = request.user
    try:
        #Check to see if the record exists by date to prevent duplicates
        recent = RecentlyViewed.objects.get(recipeID = recipe ,user=request.user)
        recent.Date = datetime.now()
        recent.save()
        print(recent)
        return JsonResponse({
            'recieved' : 'exists'
        })
    except RecentlyViewed.DoesNotExist:
        #Create a new record if it doesnt exist
        recent = RecentlyViewed(recipeID = recipe ,user=request.user,Date = datetime.now())
        recent.save()
        return JsonResponse({
            'recieved' : 'nope'
        })

def favourites(request , pk):
    user = request.user
    recipe = Recipe.objects.get(pk = request.POST['recipeID'])
    recipeName = recipe.Title

    try:
        #Check to see if the record exists by date to prevent duplicates
        Favourites.objects.get(recipeID = recipe ,user=request.user)
        return JsonResponse({
            'recieved' : 'Yes but record already exists',
            'recipe' : recipeName
        })
    except Favourites.DoesNotExist:
        newFav = Favourites(recipeID = recipe ,user=request.user,Date = datetime.now(), course = recipe.course)
        newFav.save()
        return JsonResponse({
            'recieved' : 'Yes but record doesnt exist so create',
            'recipe' : recipeName
        })

def rating(request , pk):
    user = request.user
    recipe = Recipe.objects.get(pk = request.POST['recipeID'])
    rating = request.POST['rating']
    recipeName = recipe.Title
    #print(Rated.objects.all().order_by('-rating'))

    try:
        #Check to see if the record exists by date to prevent duplicates
        reciperecord = Recipe.objects.get(pk=request.POST['recipeID'])
        reciperecord.avgRating = rating  # change field
        reciperecord.save() # this will update only
        Rated.objects.get(recipeID = recipe ,user=request.user)
        return JsonResponse({
            'recieved' : 'Yes but record already exists',
            'recipe' : recipeName
        })
    except Rated.DoesNotExist:
        newrating = Rated(recipeID = recipe ,user=request.user,Date = datetime.now(), course = recipe.course, rating = rating )
        newrating.save()
        return JsonResponse({
            'recieved' : 'Yes but record doesnt exist so create',
            'recipe' : recipeName
        })

def getRecipe(request, pk):
    user = request.user
    recipe = Recipe.objects.get(pk = pk)
    if request.user.is_authenticated:
        fav = False
        try:
            #Check to see if the record exists by date to prevent duplicates
            Favourites.objects.get(recipeID = recipe ,user=request.user)
            fav = True
        except Favourites.DoesNotExist:
            fav = False

        try:
            #Check to see if the record exists by date to prevent duplicates
            ratedRecipe = Rated.objects.get(user = request.user, recipeID = recipe)
        except Rated.DoesNotExist:
            ratedRecipe = "None"
        print(ratedRecipe)
        return render(request,'HealthyLiving/recipe_detail.html',
        {'recipe' : recipe,'favourite':fav, 'rated':(ratedRecipe),
         "ingredients": (recipe.directions.split('.,'))})
    else:
        return render(request,'HealthyLiving/recipe_detail.html',{'recipe' : recipe,})

def recipes(request):
    return render(request,'HealthyLiving/recipes.html',foodContext)

def healthdata(request):
    try:
        Hd = HealthData.objects.filter(user = request.user).latest('id')
        data = {
            'Date' : Hd.date,
            'Calories' : Hd.calories,
            'Steps' : Hd.steps,
            'Deep' : Hd.deep,
            'Light' : Hd.light,
            'ReM' : Hd.REM,
            'Wake' : Hd.Wake,
            'Totaltime' : Hd.Totaltime,
        }

        return render(request,'HealthyLiving/healthdata.html',data)

    except HealthData.DoesNotExist:
        data = {
            'Date' : 0,
            'Calories' : 0,
            'Steps' : 0,
            'Deep' : 0,
            'Light' : 0,
            'ReM' : 0,
            'Wake' : 0,
            'Totaltime' : 0,
        }
        return render(request,'HealthyLiving/healthdata.html',data)

def healthdata1(request):
    #Grab the data from the JSON PUT request from ajax in front end
    user = request.user
    Deep = request.POST['Deep']
    Light = request.POST['Light']
    REM = request.POST['REM']
    Wake = request.POST['Wake']
    totalMinutesAsleep = request.POST['totalMinutesAsleep']
    date = request.POST["date"]

    try:
        #Check to see if the record exists by date to prevent duplicates
        HealthData.objects.get(user=request.user,date=date)
        return JsonResponse({
            'deep' : Deep,
            'light' : Light,
            'rem' : REM,
            'wake' : Wake,
            'totaltime' : totalMinutesAsleep
        })
    except HealthData.DoesNotExist:
        #Create a new record if it doesnt exist
        Hd = HealthData(user=request.user,
        date=date,steps=0,
        calories=0,deep=Deep,
        light=Light,REM=REM,
        Wake=Wake,Totaltime=totalMinutesAsleep)
        Hd.save()
        return JsonResponse({
            'deep' : Deep,
            'light' : Light,
            'rem' : REM,
            'wake' : Wake,
            'totaltime' : totalMinutesAsleep
        })

def healthdata2(request):
    user = request.user
    calories = request.POST['Calories']
    Steps = request.POST['Steps']
    date = request.POST["date"]

    try:
        #Check to see if the record exists by date to prevent duplicates
        hd = HealthData.objects.get(user=request.user,date=date)
        hd.calories = calories
        hd.steps = Steps
        hd.save()
        print(hd.calories)
        return JsonResponse({
            'calories' : calories,
            'Steps' : Steps,
            'date' : date
        })
    except HealthData.DoesNotExist:
        return JsonResponse({
            'calories' : calories,
            'Steps' : Steps,
            'date' : date
        })
