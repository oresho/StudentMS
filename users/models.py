from django.db import models


class Student(models.Model):
    fullname = models.CharField(max_length=30)
    courses = models.ManyToManyField('home.Course', related_name='students')

    def __str__(self):
        return self.fullname


class Teacher(models.Model):
    fullname = models.CharField(max_length=30)
    courses = models.ManyToManyField('home.Course', related_name='teachers')

    def __str__(self):
        return self.fullname
