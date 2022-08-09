from django.urls import path, include
from .views import *

urlpatterns = [
    path("", student_home, name="student_home"),
]
