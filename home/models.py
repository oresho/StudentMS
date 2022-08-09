from weakref import proxy
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"
        ADMIN = "ADMIN", "Admin"

    base_role = Role.ADMIN

    role = models.CharField(
        "Role", max_length=10, choices=Role.choices, default=base_role
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    @property
    def profile(self):
        if self.role == User.Role.STUDENT:
            return self.studentprofile
        if self.role == User.Role.TEACHER:
            return self.teacherprofile



class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name
