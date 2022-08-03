from django.test import TestCase
from .models import (
    Student,
    StudentProfile,
    Teacher,
    TeacherProfile,
    Course,
    Subject,
    User,
)


class TestCreateStudent(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_student = Student.objects.create(
            username="test_student",
            first_name="John",
            last_name="Doe",
            email="joseph@example.com",
            password="password",
        )
        test_teacher = Teacher.objects.create(
            username="test_teacher",
            first_name="John",
            last_name="Doe",
            email="a@a.com",
            password="password",
        )
        test_course = Course.objects.create(
            name="Test Course",
        )
        test_subject = Subject.objects.create(
            name="Test Subject",
            course=test_course,
            teacher=test_teacher.teacherprofile,
        )

    def test_student_profile_creation(self):
        test_student = Student.student.get(id=1)
        test_student_profile = StudentProfile.objects.get(student=test_student)
        self.assertEqual(test_student.profile, test_student_profile)
        self.assertEqual(test_student.welcome(), "Only for students")
        self.assertEqual(test_student_profile.name, "")
        self.assertEqual(test_student_profile.surname, "")

        # Teacher
        test_teacher = Teacher.teacher.get(id=2)
        test_teacher_profile = TeacherProfile.objects.get(teacher=test_teacher)
        self.assertEqual(test_teacher_profile.name, None)
        self.assertEqual(test_teacher_profile.surname, None)
        self.assertEqual(test_student.role, User.Role.STUDENT)
        self.assertEqual(StudentProfile.objects.count(), 1)
        self.assertEqual(StudentProfile.objects.first().student, test_student)
        self.assertEqual(test_teacher.role, User.Role.TEACHER)
        self.assertEqual(TeacherProfile.objects.count(), 1)
        self.assertEqual(TeacherProfile.objects.first().teacher, test_teacher)
