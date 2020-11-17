from django.shortcuts import render, HttpResponse, redirect
from .models import  User, Destination
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    errors= User.objects.userValidation(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash1=bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    #create in database
        newUser=User.objects.create(first_name=request.POST['fname'], last_name= request.POST['lname'], email=request.POST['email'], password= hash1)
        request.session['loggedInID']=newUser.id
        return redirect('/travels')

def login(request):
    errors= User.objects.LoginValidation(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        userEmailMatch= User.objects.get(email=request.POST['email'])
        request.session['loggedInID']= userEmailMatch.id
    return redirect('/travels',)

def travels(request):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    context={
        'user':User.objects.get(id=request.session['loggedInID']),
        'allPlaces':Destination.objects.all(),
        'addedDestination':Destination.objects.filter(travelers=User.objects.get(id=request.session['loggedInID'])),
        'nonAddedDestination':Destination.objects.exclude(travelers =User.objects.get(id=request.session['loggedInID']))
    }
    return render (request, 'travels.html', context)

def logOut(request):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    request.session.clear()
    return redirect('/')

def addtrip(request):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    return render(request, 'add.html')

def add(request):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    errors= Destination.objects.tripValidator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/addtrip')
    else:
        newJob=Destination.objects.create(job=request.POST['Job'], travel_date_from= request.POST['Start'], travel_date_to= request.POST['End'], plan= request.POST['Plan'], planned_trip=User.objects.get(id=request.session['loggedInID']))
        Destination.objects.get(id=newJob.id).travelers.add(User.objects.get(id=request.session['loggedInID']))
        return redirect('/travels')

def join(request,destinationID):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    Destination.objects.get(id=destinationID).travelers.add(User.objects.get(id=request.session['loggedInID']))
    return redirect('/travels')

def cancel(request,destinationID):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    Destination.objects.get(id=destinationID).travelers.remove(User.objects.get(id=request.session['loggedInID']))
    return redirect('/travels')

def destinationInfo(request,destinationID):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    context={
        'job': Destination.objects.get(id=destinationID),
    }
    return render(request,'destinationInfo.html',context)

def delete(request,destinationID):
    if 'loggedInID' not in request.session:
        messages.error(request,"You must be logged in")
        return redirect('/')
    c=Destination.objects.get(id=destinationID)
    c.delete()
    return redirect('/travels')

# Create your views here.
