from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Instructor, Student, Course, Assignment, Submission
from uuid import UUID
from . import design_tool
import numpy as np

def home(request):
    return render(request, "main/home.html")


def test(request):
    num, den, omega, mag, phase, gm, pm, wg, wp= design_tool.Gs()
    if request.method == "POST":
        if request.POST.get("zero"):
            z = float(request.POST.get("zero"))
            p = float(request.POST.get("pole"))
            k = float(request.POST.get("gain"))
            z = np.array([z])
            p = np.array([p])
            omega_comp, mag_comp, phase_comp, gm, pm, wp, wg  = design_tool.zpk(z,p, k)
        if request.POST.get("p"):
            p = request.POST.get("p")
            i = request.POST.get("i")
            d = request.POST.get("d")
            if not i:
                i = 0
            if not d:
                d = 0
            p = float(p)
            i = float(i)
            d = float(d)
            omega_comp, mag_comp, phase_comp, gm, pm, wp, wg  = design_tool.pid(p, i, d)
        return render(request, "main/test.html", {
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": 'Servo Motor',
                "numerator": num,
                "denominator": den,
                "mag_comp": mag_comp,
                "ph_comp": phase_comp,
                "omega_comp":omega_comp
            })
    return render(request, "main/test.html", {
                
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": 'Servo Motor',
                "numerator": "3",
                "denominator": "3s^2 +1",
                "pm": pm,
                "gm": gm
            })

def register(request):
    try: # Check if already logged in and have an account
        user = User.objects.get(username=request.user)
        return HttpResponseRedirect(reverse("home"))
    except :
        if request.method == "POST":
            username = request.POST.get("username")
            first=request.POST.get("first")
            last=request.POST.get("last")
            major= request.POST.get("major")
            email = request.POST.get("email")
            code=request.POST.get("code")
            agree=request.POST.get("agree")
            password = request.POST.get("password")
            confirmation = request.POST.get("confirmation")
            # Attempt to create new user
            # If the user is an instructor
            if request.POST.get("instructor"):
                # Ensure all fields are filled correctly
                if not password or not email or not username or not first or not last:
                    return render(request, "main/register.html", {
                        "instMSG": "Make sure all fields are filled.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "major": major,
                        "email": email,
                    })
                # Ensure password matches confirmation
                if password != confirmation:
                    return render(request, "main/register.html", {
                        "instMSG": "Passwords must match.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "major": major,
                        "email": email,
                    })
                # Ensure that the user agrees to all terms and privacy policy
                if not request.POST.get("agree")=="on":
                    return render(request, "main/register.html", {
                        "instMSG": "You need to agree on the terms in order to sign up.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "major": major,
                        "email": email,
                    })
                try:
                    user = User.objects.create_user(username, email, password,status="i",first_name=first,last_name=last)
                    user.save()
                    instructor=Instructor.objects.create(credentials=user,major=major)
                    instructor.save()
                except:
                    return render(request, "main/register.html", {
                        "instMSG": "Username already taken.",
                        "first": first,
                        "last": last,
                        "major": major,
                        "email": email,
                    })
            # If the user is a student
            elif request.POST.get("student"):
                # Ensure all fields are filled correctly
                if not password or not email or not username or not first or not last:
                    return render(request, "main/register.html", {
                        "studMSG": "Make sure all fields are filled.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
                    })
                # Ensure password matches confirmation
                if password != confirmation:
                    return render(request, "main/register.html", {
                        "studMSG": "Passwords must match.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
                    })
                # Ensure that the user agrees to all terms and privacy policy
                if not request.POST.get("agree")=="on":
                    return render(request, "main/register.html", {
                        "studMSG": "You need to agree on the terms in order to sign up.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
                   })  
                try: # Creating New User
                    try : # Check if the Course Code is valid.
                        temp = UUID(code,version=4)
                    except:
                        return render(request, "main/register.html", {
                        "studMSG": "Make sure that your course code is valid.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
                    })
                    course=Course.objects.get(code=code)
                    user = User.objects.create_user(username, email, password,status="s",first_name=first,last_name=last)
                    user.save()
                    student=Student.objects.create(credentials=user,courses=course)
                    student.save()
                except:
                    return render(request, "main/register.html", {
                        "studMSG": "Username already taken.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
                    })
                if not code:
                    return render(request, "main/register.html", {
                        "studMSG": "Make sure to enter your course code correctly.",
                        "username": username,
                        "first": first,
                        "last": last,
                        "code": code,
                        "email": email,
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

def student(request):
    if request.POST.get("assignment"):
        assignId=request.POST.get("assignment")
        request.session["id"]=assignId
        assignment  = Assignment.objects.get(id=assignId)
        if assignment.simulator=="Servo Motor":
            return HttpResponseRedirect(reverse(servomotor))
        elif assignment.simulator=="Cruise Control":
            return HttpResponseRedirect(reverse(cruise))
        elif assignment.simulator=="Adaptive cruise Control":
            return HttpResponseRedirect(reverse(adaptive))
    try:
        assignments=[]
        student=Student.objects.get(credentials=request.user)
        for something in student.courses.assignments.filter():
            assignments.append(something)
    except:
        return HttpResponseRedirect(reverse("home"))
    return render(request,"main/student.html",{
            "student":student,
            "assignments": assignments
        }) 

def instructor(request):
    req= request.POST
    try:    
        instructor= Instructor.objects.get(credentials=request.user)
    except:
        return HttpResponseRedirect(reverse("home"))
    courses=[]
    assignments=[]
    simulators=[]
    courseAssignments=[] #Assignment in each course 
    courseAssignment={} #course:assignment pairs
    assignmentSubmissions=[] #Submissions in each assignment
    assignmentSubmission={} #Assignment:submissions pairs
    course=Course.objects.filter(instructor=request.user)
    assignment=Assignment.objects.filter(instructor=request.user)
    for something in course:
        courses.append(something.name)
        for assign in something.assignments.all():
            courseAssignments.append(assign.subject)
            for submission in Submission.objects.filter(assignment=assign):
                assignmentSubmissions.append(submission)
            assignmentSubmission[f"{something.name}:{assign.subject}"]=assignmentSubmissions[:]
            assignmentSubmissions.clear()
        courseAssignment[something.name]=courseAssignments[:]
        courseAssignments.clear()
    for something in assignment:
        assignments.append(something)    
    for choice in Assignment.simulator_choices:
        simulators.append(choice[0])
    if req:
        if req.get("sim"):
            sim = req.get("sim")
            course = req.get("course")
            due = req.get("due")
            subject = req.get("assignmentSubject")
            rise = req.get("rise")
            settle = req.get("settle")
            overshoot = req.get("overshoot")
            error = req.get("error")
            desc = req.get("desc")
            controller= req.get("controller")
            if req.get("grade")=="auto": 
                assign=Assignment.objects.create(subject=subject,dueDate=due,simulator=sim,score=4,instructor=request.user.username,riseTime=rise,setTime=settle,pOvershoot=overshoot,Ess=error,controller=controller)
                assign.save()
            elif req.get("grade")=="receive":
                assign=Assignment.objects.create(subject=subject, dueDate=due, simulator=sim, score=4, instructor=request.user.username,describtion=desc,controller=controller)
                assign.save()
            course=Course.objects.get(name=course)
            course.assignments.add(assign)
            return HttpResponseRedirect(reverse("instructor"))
        if req.get("courseName"):
            courseName = req.get("courseName")
            course=Course.objects.create(name=courseName, instructor=request.user)
            course.save
            return HttpResponseRedirect(reverse("instructor"))
    else:
        return render(request, "main/instructor.html", {
            "instructor": instructor,
            "assignments": assignments,
            "simulators": simulators,
            "courseAssignment": courseAssignment,
            "courses": courses,
            "assignmentSubmission": assignmentSubmission,
        })


def cruise(request):
    try:
        assignment = Assignment.objects.get(id=request.session["id"])
        if assignment.simulator=="Cruise Control":
            return render(request, "main/cruise.html", {
                "assignment": assignment,
            })
        else:
            return render(request, "main/cruise.html", {
            })
    except:
        controller = ""
    return render(request, "main/cruise.html", {
        "controller": controller,
    })


def adaptive(request):
    try:
        assignment = Assignment.objects.get(id=request.session["id"])
        return render(request, "main/adaptive.html", {
            "assignment": assignment,
        })
    except:
        controller = ""
    return render(request, "main/adaptive.html", {
        "controller": controller,
    })


def servomotor(request):
    if request.POST:
        zero = request.POST.get("zero")
        pole = request.POST.get("pole")
        gain = request.POST.get("gain")
        p = request.POST.get("p")
        i = request.POST.get("i")
        d = request.POST.get("d")
        submit= request.POST.get("submit")
        if submit==1:
            if p and not i and not d:
                return
            if p and d and not i:
                return
        else:
            if p and not i and not d:
                return
            if p and d and not i:
                return
    try:
        assignment = Assignment.objects.get(id=request.session["id"])
        return render(request, "main/servomotor.html", {
            "assignment": assignment,
        })
        if assignment.simulator=="Servo Motor":
            return render(request, "main/cruise.html", {
                "assignment": assignment,
            })
        else:
            return render(request, "main/cruise.html", {
            })
    except:
        controller = ""
    return render(request, "main/servomotor.html", {
        "controller": controller,
    })
