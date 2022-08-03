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
    course = models.ManyToManyField("course", blank=True, related_name="students")

    def __str__(self):
        return self.student.username


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


class Teacher(User):

    base_role = User.Role.TEACHER

    teacher = TeacherManager()

    @property
    def profile(self):
        return self.teacherprofile

    class Meta:
        proxy = True


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(
        Teacher,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="teacherprofile",
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    course = models.ManyToManyField("course", blank=True, related_name="teachers")

    def __str__(self):
        return self.teacher.username


@receiver(post_save, sender=Teacher)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TEACHER:
        TeacherProfile.objects.create(teacher=instance)


@receiver(post_save, sender=Teacher)
def save_teacher_profile(sender, instance, **kwargs):
    instance.teacherprofile.save()


# TODO change subject to course


class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.name
