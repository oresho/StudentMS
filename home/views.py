from tkinter import E
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login as auth_login

from .forms import UserLoginForm
from student.models import Student

# Create your views here.
def home(request):
    return render(request, "home/index.html")


def login(request):
    if request.method == "POST":
        # get and clean the data
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            if user.role == "STUDENT":
                return redirect("student_home")
            return redirect("home")
        else:
            return redirect("login")
    else:
        return render(request, "home/login.html")


def signup(request):
    if request.method == "POST":
        # get and clean the data
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        # create the user
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        else:
            try:
                student = Student.objects.create(username=username, password=password)
            except IntegrityError as e:
                student = Student.objects.get(username=username)
                print(student)
            print(student)
            auth_login(request, student)
            return redirect("student_home")

    else:
        return render(request, "home/signup.html")
