import imp
from django.urls import path, include
from .views import *


urlpatterns = [
    path("", home, name="home"),
    path("login/", login, name="login"),
]
