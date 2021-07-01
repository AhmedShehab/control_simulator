from os import remove
from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from scipy.linalg.basic import pinv
from .models import User, Instructor, Student, Course, Assignment, Submission
from uuid import UUID
from . import design_tool
import numpy as np
from .systems import *
from datetime import date
import decimal

def home(request):
    return render(request, "main/home.html",{
        "home": True
    })

def design(request):
    name = request.GET.get("name")
    sys = name
    if sys == "Servomotor":
        sys = "servo"
    elif sys == "Cruise":
        sys = "servo"
    empty = False
    if name != None:
        omega, mag, phase = bode_sys(sys)
        num, den = tf(sys)
        gm, pm, wg, wp = margin_sys(sys)
    else:
        name = "Design By Frequency"
        num = "1"
        den = "s + 1"
        print("R ", num, "d", den)
        empty = True
        n = [1]
        d = [1,1]
        del request.session['n']
        del request.session['d']
        request.session['n'] = n
        request.session['d'] = d
        Gs = control.tf(n, d)
        omega, mag, phase = bode_sys(Gs)
        gm, pm, wg, wp = margin_sys(Gs)
        sys = Gs
    remember = 1
    if request.method == "POST":
        zero = float(request.POST.get("zero",0))
        pole = float(request.POST.get("pole",0))
        gain = float(request.POST.get("gain",0))
        p = float(request.POST.get("p",0))
        i = float(request.POST.get("i",0))
        d = float(request.POST.get("d",0))
        remember = request.POST.get("remember",0)
        if request.POST.get("num"):
            n = request.POST.get("num")
            d = request.POST.get("den")
            n = n.strip('][').split(',')
            d = d.strip('][').split(',')
            try:
                n = [float(i) for i in n]
                d = [float(i) for i in d]
                for i in range(len(n)):
                    if n[i].is_integer():
                        n[i] = int(n[i])
                for i in range(len(d)):
                    if d[i].is_integer():
                        d[i] = int(d[i])
                num = arrayToString(n)
                den = arrayToString(d)
                Gs = control.tf(n, d)
                omega, mag, phase = bode_sys(Gs)
                gm, pm, wg, wp = margin_sys(Gs)
                del request.session['n']
                del request.session['d']
                request.session['n'] = n
                request.session['d'] = d
                return render(request, "main/design.html", {
                        "omega": omega,
                        "ph": phase,
                        "mag": mag,
                        "name": 'Design By Frequency',
                        "numerator": num,
                        "denominator": den,
                        "design": True,
                        "empty": empty
                    })
            except:
                return render(request, "main/design.html", {
                    "omega": omega,
                    "ph": phase,
                    "mag": mag,
                    "name": 'Design By Frequency',
                    "numerator": num,
                    "denominator": den,
                    "design": True,
                    "empty": empty,
                    "error": True
                })
        n = request.session[n]
        d = request.session[d]
        num = arrayToString(n)
        den = arrayToString(d)
        Gs = control.tf(n, d)
        omega, mag, phase = bode_sys(Gs)
        gm, pm, wg, wp = margin_sys(Gs)
        sys = Gs
        if request.POST.get("zero"):
            omega_comp, mag_comp, phase_comp = bode_zpk(sys, zero, pole, gain)
            gm_comp, pm_comp, wg_comp, wp_comp = margin_zpk(sys, zero, pole, gain)
        if request.POST.get("p"):
            print(i)
            if not i:
                i = 0
            if not d:
                d = 0
            omega_comp, mag_comp, phase_comp = bode_pid(sys, p, i, d)
            gm_comp, pm_comp, wg_comp, wp_comp = margin_pid(sys, p, i, d)
        return render(request, "main/design.html", {
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": name,
                "numerator": num,
                "denominator": den,
                "mag_comp": mag_comp,
                "ph_comp": phase_comp,
                "omega_comp":omega_comp,
                "pm_comp": pm_comp,
                "gm_comp": gm_comp,
                "design": True,
                "empty": empty, 
                "remember": remember
            })
    
    return render(request, "main/design.html", {
                "omega": omega,
                "ph": phase,
                "mag": mag,
                "name": name,
                "numerator": num,
                "denominator": den,
                "pm": pm,
                "gm": gm,
                "design": True,
                "empty": empty,
                "remember": remember
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
    try:
        assignments=[]
        submitted=[]
        student=Student.objects.get(credentials=request.user)
        studentSubmissions= Submission.objects.filter(student=student)
        for something in student.courses.assignments.filter():
            assignments.append(something)
        for submission in studentSubmissions:
            submitted.append(submission)
            try:
                assignments.remove(submission.assignment)
            except:
                pass
    except:
        return HttpResponseRedirect(reverse("home"))
    return render(request,"main/student.html",{
            "student":student,
            "assignments": assignments,
            "submitted":submitted,
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
                assign=Assignment.objects.create(subject=subject,dueDate=due,simulator=sim,score=5,instructor=request.user.username,riseTime=rise,setTime=settle,pOvershoot=overshoot,Ess=error,controller=controller)
                assign.save()
            elif req.get("grade")=="receive":
                assign=Assignment.objects.create(subject=subject, dueDate=due, simulator=sim, score=5, instructor=request.user.username,description=desc,controller=controller)
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
        student = Student.objects.get(credentials=request.user)
        if assignment.simulator == "Cruise Control":
            if not assignment.description:
                assignmentRequirements={
                    "RiseTime":assignment.riseTime,
                    "SettlingTime":assignment.setTime,
                    "SteadyStateError":assignment.Ess,
                    "Overshoot":assignment.pOvershoot
                }
            else:
                assignmentRequirements={
                    "Description":assignment.description
                }
            pass
        else:
            assignment=""
    except:
        assignment=""
        pass
    sys = "cruise"
    remember = 1
    setTime = 1.0
    setPoint = 1.0
    if request.POST:
        zero = float(request.POST.get("zero",0))
        pole = float(request.POST.get("pole",0))
        gain = float(request.POST.get("gain",0))
        p = float(request.POST.get("p",0))
        i = float(request.POST.get("i",0))
        d = float(request.POST.get("d",0))
        step = float(request.POST.get("step",0))
        setTime = float(request.POST.get("time",0))
        setPoint = float(request.POST.get("setPoint",0))
        remember = request.POST.get("remember",0)
        PIDController={
            "Simulator":"servo",
            "Controller":"PID",
            "StepInput":step,
            "setTime":setTime,
            "P":p,
            "I":i,
            "D":d,
        }
        ZPKController={
            "Simulator":"servo",
            "Controller":"ZPK",
            "StepInput":step,
            "setTime":setTime,
            "Zero":zero,
            "Pole":pole,
            "Gain":gain,
        }
        submit= request.POST.get("submit")
        if submit== "submit":
            del request.session["id"]
            if Submission.objects.filter(assignment=assignment):
                test = Submission.objects.filter(assignment=assignment)
                for something in test:
                    if something.student==student:
                        return render(request,"main/cruise.html",{
                            "duplicateAssignment":"Sorry you can't submit the same assignment twice",
                        })
            subDate = date.today().strftime("%Y-%m-%d")
            PIDParamaters= f"Propotional Constant(P): {p}, \n Differential Constant(D): {i}, \n Integral Constant(I): {d},"
            ZPkParamaters= f"Gain: {gain}, \n Pole: {pole}, \n Zero: {zero}"
            if p or i or d:   # PID Controller
                controller = PIDController
                parameters = PIDParamaters
            else:             # ZPK Controller
                controller = ZPKController
                parameters = ZPkParamaters
            if assignmentRequirements.get("Description",0):
                submission = Submission.objects.create(student=student,assignment=assignment,dateSubmitted=subDate,parameters=parameters)
                submission.save()
            elif assignmentRequirements.get("RiseTime"):
                score,Pass =isPass(controller,assignmentRequirements)
                submission = Submission.objects.create(student=student,assignment=assignment,score=score,Pass=Pass,dateSubmitted=subDate,parameters=parameters)
                submission.save()
            return HttpResponseRedirect(reverse("cruise"))                     
        elif submit == "simulate":
            if p:   # PID Controller
                if not i:
                    i = 0
                if not d:
                    d = 0
                t, output = step_pid(sys, setTime, setPoint, p, i, d)
            elif zero and pole and gain:
                t, output = step_zpk(sys, setTime, setPoint, zero, pole, gain)
            else:
                t, output = step_sys(sys, setTime, setPoint)
            return render(request, "main/cruise.html", {
                "assignment":assignment,
                "t": t,
                "output":output,
                "setPoint":setPoint,
                "time":setTime,
                "remember": remember,
                "p":p,
                "i":i,
                "d":d,
                "zero":zero,
                "pole":pole,
                "gain":gain
        })
    else:
        return render(request, "main/cruise.html", {
            "assignment":assignment,
            "remember":remember,
            "setPoint":setPoint,
            "time":setTime,
        })

def servomotor(request):
    try:
        assignment = Assignment.objects.get(id=request.session["id"])
        student = Student.objects.get(credentials=request.user)
        if assignment.simulator == "Servo Motor":
            if not assignment.description:
                assignmentRequirements={
                    "RiseTime":assignment.riseTime,
                    "SettlingTime":assignment.setTime,
                    "SteadyStateError":assignment.Ess,
                    "Overshoot":assignment.pOvershoot
                }
            else:
                assignmentRequirements={
                    "Description":assignment.description
                }
            pass
        else:
            assignment=""
    except:
        assignment=""
        pass
    sys = "servo"
    remember = 1
    setTime = 1.0
    setPoint = 1.0
    if request.POST:
        zero = float(request.POST.get("zero",0))
        pole = float(request.POST.get("pole",0))
        gain = float(request.POST.get("gain",0))
        p = float(request.POST.get("p",0))
        i = float(request.POST.get("i",0))
        d = float(request.POST.get("d",0))
        step = float(request.POST.get("step",0))
        setTime = float(request.POST.get("time",0))
        setPoint = float(request.POST.get("setPoint",0))
        remember = request.POST.get("remember",0)
        PIDController={
            "Simulator":"servo",
            "Controller":"PID",
            "StepInput":step,
            "setTime":setTime,
            "P":p,
            "I":i,
            "D":d,
        }
        ZPKController={
            "Simulator":"servo",
            "Controller":"ZPK",
            "StepInput":step,
            "setTime":setTime,
            "Zero":zero,
            "Pole":pole,
            "Gain":gain,
        }
        submit= request.POST.get("submit")
        if submit== "submit":
            del request.session["id"]
            if Submission.objects.filter(assignment=assignment):
                test = Submission.objects.filter(assignment=assignment)
                for something in test:
                    if something.student==student:
                        return render(request,"main/servomotor.html",{
                            "duplicateAssignment":"Sorry you can't submit the same assignment twice",
                        })
            subDate = date.today().strftime("%Y-%m-%d")
            PIDParamaters= f"Propotional Constant(P): {p}, \n Differential Constant(D): {i}, \n Integral Constant(I): {d},"
            ZPkParamaters= f"Gain: {gain}, \n Pole: {pole}, \n Zero: {zero}"
            if p or i or d:   # PID Controller
                controller = PIDController
                parameters = PIDParamaters
            else:             # ZPK Controller
                controller = ZPKController
                parameters = ZPkParamaters
            if assignmentRequirements.get("Description",0):
                submission = Submission.objects.create(student=student,assignment=assignment,dateSubmitted=subDate,parameters=parameters)
                submission.save()
            elif assignmentRequirements.get("RiseTime"):
                score,Pass =isPass(controller,assignmentRequirements)
                submission = Submission.objects.create(student=student,assignment=assignment,score=score,Pass=Pass,dateSubmitted=subDate,parameters=parameters)
                submission.save()
            return HttpResponseRedirect(reverse("servomotor"))                     
        elif submit == "simulate":
            if p:   # PID Controller
                if not i:
                    i = 0
                if not d:
                    d = 0
                t, output = step_pid(sys, setTime, setPoint, p, i, d)
            elif zero and pole and gain:
                t, output = step_zpk(sys, setTime, setPoint, zero, pole, gain)
            else:
                t, output = step_sys(sys, setTime, setPoint)
            return render(request, "main/servomotor.html", {
                "assignment":assignment,
                "t": t,
                "output":output,
                "setPoint":setPoint,
                "time":setTime,
                "remember": remember,
                "p":p,
                "i":i,
                "d":d,
                "zero":zero,
                "pole":pole,
                "gain":gain
        })
    else:
        return render(request, "main/servomotor.html", {
            "assignment":assignment,
            "remember":remember,
            "setPoint":setPoint,
            "time":setTime,
        })
 