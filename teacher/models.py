from weakref import proxy
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


from home.models import User, Course


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
    course = models.ManyToManyField(Course, blank=True, related_name="teachers")

    def __str__(self):
        return self.teacher.username


@receiver(post_save, sender=Teacher)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == User.Role.TEACHER:
        TeacherProfile.objects.create(teacher=instance)


@receiver(post_save, sender=Teacher)
def save_teacher_profile(sender, instance, **kwargs):
    instance.teacherprofile.save()
