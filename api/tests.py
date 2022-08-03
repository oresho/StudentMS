from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from home.models import Student, StudentProfile


class StudentTest(APITestCase):
    def test_view_student_list(self):
        url = reverse("list_student")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


