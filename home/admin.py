from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Course
from student.models import Student, StudentProfile
from teacher.models import Teacher, TeacherProfile


class StudentInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    verbose_name_plural = "studentprofile"


class TeacherInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    verbose_name_plural = "teacherprofile"


class StudentAdmin(BaseUserAdmin):
    inlines = (StudentInline,)


class TeacherAdmin(BaseUserAdmin):
    inlines = (TeacherInline,)


admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(StudentProfile)
admin.site.register(Course)
