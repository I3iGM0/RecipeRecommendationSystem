from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import datetime
from Users.models import Profile,HealthData

# Create your views here.

posts = [
    {
        'author':'Mohamed',
        'title':'Mo'
    },
    {
        'author':'Ahmed',
        'title':'A'
    }
]

def home(request):

    contexts = {
        'posts':posts
    }

    return render(request,'HealthyLiving/home.html',contexts)


def about(request):
    return render(request,'HealthyLiving/about.html')

def fitbit(request):
    return render(request,'HealthyLiving/fitbit.html')

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
