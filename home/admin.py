from attr import fields
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Student, Teacher, StudentProfile, TeacherProfile, Course, Subject


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
admin.site.register(Course)
admin.site.register(Subject)
