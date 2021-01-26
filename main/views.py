from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Instructor,Student,Course,Assignment
from uuid import UUID
# Create your views here.
def home(request):
    return render(request, "main/home.html")

def register(request):
    try: # Check if already logged in and have an account
        user = User.objects.get(username=request.user)
        return HttpResponseRedirect(reverse("home"))
    except :
        if request.method == "POST":
            username = request.POST["username"]
            major= request.POST["major"]
            email = request.POST["email"]
            code=request.POST["code"]
            agree=request.POST.get("agree")
            password = request.POST["password"]
            confirmation = request.POST["confirmation"]
            # Ensure all fields are filled correctly
            if not password or not email or not username:
                return render(request, "main/register.html", {
                    "message": "Make sure all fields are filled."
                })
            # Ensure password matches confirmation
            if password != confirmation:
                return render(request, "main/register.html", {
                    "message": "Passwords must match."
                })
            if request.POST.get("student") and not code:
                return render(request, "main/register.html", {
                    "message": "Make sure to enter your course code correctly."
                })

            # Ensure that the user agrees to all terms and privacy policy
            if not request.POST.get("agree")=="on":
                return render(request, "main/register.html", {
                    "message": "You need to agree on the terms in order to sign up."
                })
            # Attempt to create new user
            # If the user is an instructor
            if request.POST.get("instructor"):
                try:
                    user = User.objects.create_user(username, email, password,status="i")
                    user.save()
                    instructor=Instructor.objects.create(credentials=user,major=major)
                    instructor.save()
                except IntegrityError:
                    return render(request, "main/register.html", {
                        "message": "Username already taken."
                    })
            # If the user is a student
            elif request.POST.get("student"):
                try: # Creating New User
                    try : # Check if the Course Code is valid.
                        temp = UUID(code,version=4)
                    except:
                        return render(request, "main/register.html", {
                        "message": "Make sure that your course code is valid."
                    })
                    course=Course.objects.get(code=code)
                    user = User.objects.create_user(username, email, password,status="s")
                    user.save()
                    student=Student.objects.create(credentials=user,courses=course,major=major)
                    student.save()
                except IntegrityError:
                    return render(request, "main/register.html", {
                        "message": "Username already taken."
                    })
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/register.html")

def login_view(request):
    if request.method == "POST":
        print(request.POST)
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))

def student(request):
    try:
        assignments=[]
        user=request.user
        student=Student.objects.get(credentials=user)
        for something in student.assignments.all():
            assignments.append(something)
        return render(request,"main/student.html",{
            "student":student,
            "assignments": assignments
        })
    except:
        return HttpResponseRedirect(reverse("home")) 

def instructor(request):
    if request.POST: 
        # Reminder: Check if there are missing fields
        sim = request.POST.get("sim")
        desc = request.POST.get("desc")
        due = request.POST.get("due")
        subject = request.POST.get("subject")
        assign=Assignment.objects.create(subject=subject,dueDate=due,simulator=sim,describtion=desc,score=5,instructor=request.user.username)
        assign.save()
        return HttpResponseRedirect(reverse("instructor")) 
    else:
        assignments = []
        simulators=[]
        assignment=Assignment.objects.filter(instructor=request.user.username)
        i=0
        for something in assignment:
            assignments.append(something)
        for choice in Assignment.simulator_choices:
            simulators.append(choice[0])
        try:
            user=request.user    
            instructor= Instructor.objects.get(credentials=user)
            return render(request,"main/instructor.html",{
                "instructor":instructor,
                "assignments": assignments,
                "simulators": simulators
            })
        except:
            return HttpResponseRedirect(reverse("home")) 


def cruise(request):
    return render(request,"main/cruise.html")
def adaptive(request):
    return render(request,"main/adaptive.html")