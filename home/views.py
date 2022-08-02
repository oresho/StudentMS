from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login

from .forms import UserLoginForm

# Create your views here.
def home(request):
    return render(request, 'home/index.html')


def login(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'home/login.html', {'form': form})