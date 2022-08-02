from django.test import TestCase
from .models import Student, StudentProfile, Teacher, TeacherProfile, Course, Subject, User


class TestCreateStudent(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_student = Student.objects.create(
            first_name="John",
            last_name="Doe",
            email="joseph@example.com",
            password="password",
        )
        test_teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="a@a.com",
            password="password",
        )
        test_course = Course.objects.create(
            name="Test Course",
            teacher=test_teacher,
        )
        test_subject = Subject.objects.create(
            name="Test Subject",
            course=test_course,
        )

        def test_student_profile_creation(self):
            self.assertEqual(test_student.role, User.Role.STUDENT)
            self.assertEqual(StudentProfile.objects.count(), 1)
            self.assertEqual(StudentProfile.objects.first().student, test_student)
            self.assertEqual(test_teacher.role, User.Role.TEACHER)
            self.assertEqual(TeacherProfile.objects.count(), 1)
            self.assertEqual(TeacherProfile.objects.first().teacher, test_teacher)
