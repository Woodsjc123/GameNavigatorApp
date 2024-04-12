from rest_framework.test import APITestCase
from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

class LoginAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testinguser', email='test@example.com', password='testpassword')
        self.login_url = reverse('api_login')

    def test_login_success(self):
        data = { 'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_fail(self):
        data = {'username': 'testinguser','password': 'wrongpassword'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)