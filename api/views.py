from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from student.models import Student
from .serializers import StudentSerializer


class StudentList(generics.ListCreateAPIView):
    queryset = Student.student.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.student.all()
    serializer_class = StudentSerializer
