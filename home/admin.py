from django.contrib import admin
from .models import Student, Teacher, StudentProfile, TeacherProfile, Course, Subject

# Register your models here.
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentProfile)
admin.site.register(TeacherProfile)
admin.site.register(Course)
admin.site.register(Subject)

