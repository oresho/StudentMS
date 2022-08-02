from weakref import proxy
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

# class Course(models.Model):
#     course_code = models.CharField(max_length=20)

#     def __str__(self):
#         return self.course_code


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


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)

    # def create_user(self, email, date_of_birth, password=None):
    #     """
    #     Creates and saves a User with the given email, date of
    #     birth and password.
    #     """
    #     if not email:
    #         raise ValueError('Users must have an email address')
    #     user = self.model(
    #         email=self.normalize_email(email),
    #         date_of_birth=date_of_birth,
    #     )
    #     user.set_password(password)
    #     user.save(using=self._db)
    #     return user


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


class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="")
    surname = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True)
    course = models.ForeignKey("course", on_delete=models.SET_NULL, null=True)

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

    def welcome(self):
        return "Only for teachers"


class TeacherProfile(models.Model):
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='teacherprofile')
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.teacher.username


@receiver(post_save, sender=Teacher)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TEACHER:
        TeacherProfile.objects.create(teacher=instance)


class Subject(models.Model):
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE)
    course = models.ForeignKey("course", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
