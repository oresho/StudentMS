from weakref import proxy
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

from home.models import User, Course


# Create your models here.

class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):

    base_role = User.Role.STUDENT

    student = StudentManager()

    @property
    def profile(self):
        return StudentProfile.objects.get(student=self)

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for students"


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.STUDENT:
        StudentProfile.objects.create(student=instance)


@receiver(post_save, sender=Student)
def save_student_profile(sender, instance, **kwargs):
    instance.studentprofile.save()


class StudentProfile(models.Model):
    student = models.OneToOneField(
        Student,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="studentprofile",
    )
    name = models.CharField(max_length=100, default="")
    surname = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True)
    program = models.CharField(max_length=100, blank=True)
    course = models.ManyToManyField(Course, blank=True, related_name="students")

    def __str__(self):
        return self.student.username

