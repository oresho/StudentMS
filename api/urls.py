from django.urls import path
from . import views

urlpatterns = [
    path("student/<int:pk>/", views.StudentDetail.as_view(), name="student_detail"),
    path("", views.StudentList.as_view(), name="list_student"),
]
