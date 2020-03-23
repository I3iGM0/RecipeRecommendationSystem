from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.generic import ListView, DetailView
from django.utils.timezone import now
from django.utils.timezone import datetime

#Import models
from Users.models import Profile,HealthData
from .models import Recipe,RecentlyViewed
from Users.models import Profile

#import python libraries
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# Create your views here.

df = pd.read_csv("/Users/mohamed/Documents/Recommendation/CleanedRecipe.csv" ,sep = ',')
df = df[['title','categories','ingredients','directions','calories','words']]
custom  = df[['title','categories','ingredients','directions','calories']]
#Create matrix
count = CountVectorizer()
count_matrix = count.fit_transform(df['words'])
#cosine_sim = cosine_similarity(count_matrix, count_matrix)

array = []
for i in custom['title']:
    array.append(i)

def recommend(food):
    idx = array.index(food)
    #Compute similarity
    cosine_sim = cosine_similarity(count_matrix[idx], count_matrix)
    cosine_sim
    #Store the similarity
    ls = []
    ls = cosine_sim
    #Create a 2D array for recipe alongside its similarity
    foodarray = []
    for i in range(len(array)):
        foodarray.append([i,array[i],ls[0][i]])

    foodarray.sort(key=lambda x:x[2],reverse=True)
    return foodarray[1:11]



def home(request):
    if not request.user.is_authenticated:
        return render(request,'HealthyLiving/home.html')

    try:
        #Check to see if the record exists by date to prevent duplicates
        recent = RecentlyViewed.objects.filter(user = request.user).latest('id')
        #print(RecentlyViewed.objects.filter(user = request.user).last())
        #print(RecentlyViewed.objects.filter(user = request.user).first())
        print(recent)
        #recent = RecentlyViewed.objects.filter(user = user)[0]
        ls = recommend(recent.recipeID.Title)
        #print(ls)
        foodLs = []
        foodContext = {}
        for i in range(len(ls)):
            id = int(ls[i][0] + 1)
            #print(str(ls[i][0]))
            #print(Recipe.objects.get(pk=id).directions)
            #print(list(Recipe.objects.get(pk=id).categories.split(',')))
            foodLs.append(Recipe.objects.get(pk=id))
        #first = int(ls[0][0]+1)
        #print(first)
        #print(foodLs)
        foodContext = {
            'Recipe' : list(foodLs)
        }

        return render(request,'HealthyLiving/home.html',foodContext)

    except RecentlyViewed.DoesNotExist:
        foodContext = {
            'Recipe' : 'None'
        }

        return render(request,'HealthyLiving/home.html',foodContext)

def test(request):
    return render(request,'HealthyLiving/test.html')

class PostListView(ListView):
    model = Recipe
    template_name = 'HealthyLiving/recipes.html'
    queryset = Recipe.objects.all()
    context_object_name = 'Recipe'
    paginate_by = 9

class PostDetailView(DetailView):
    model = Recipe

def recentlyVisited(request , pk):
    recipe = Recipe.objects.get(pk = request.POST['recipeID'])
    recipeName = recipe.Title
    user = request.user
    try:
        #Check to see if the record exists by date to prevent duplicates
        RecentlyViewed.objects.get(recipeID = recipe ,user=request.user)
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

def getRecipe(request, pk):
    recipe = Recipe.objects.get(pk = pk)
    return render(request,'HealthyLiving/recipe_detail.html',{'recipe' : recipe})

def recipes(request):
    return render(request,'HealthyLiving/recipes.html',foodContext)

def fitbit(request):
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

        return render(request,'HealthyLiving/fitbit.html',data)

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
        return render(request,'HealthyLiving/fitbit.html',data)



def fitbit1(request):
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

def fitbit2(request):
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
