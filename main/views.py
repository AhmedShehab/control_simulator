from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User,Instructor,Student,Course
from uuid import UUID
# Create your views here.
def home(request):
    return render(request, "main/home.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
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
                user = User.objects.create_user(username, email, password)
                user.save()
                instructor=Instructor.objects.create(credentials=user).save()
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
                course=Course.objects.filter(code=code)
                user = User.objects.create_user(username, email, password).save()
                student=Student.objects.create(credentials=user).save()
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