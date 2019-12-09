from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# url should constant
CREATE_USER_URL = reverse('user:create')


def create_user(**param):
    """The Function Return User Model"""
    return get_user_model().object.create_user(**param)


class PublicUserApiTests(TestCase):
    """Test User Api Public"""

    def setUp(self):
        """Set Up Client To Variable"""
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test Create User Valid Payload Success"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test_pass@123',
            'name': 'Test Name',
            }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Testing user has been create correctly
        user = get_user_model().object.get(**res.data)
        self.assertTrue(
            user.check_password(payload['password'])
            )
        # Check Password No Return in object
        self.assertNotIn('password', res.data)

    def test_user_exist(self):
        """Test That user Create Already Exists Fails"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test_pass@123',
            'name': 'Test Name'
            }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test Password Must Be More Than 8 Character"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'tes',
            'name': 'Test Name'
            }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exist = get_user_model().object.filter(email=payload['email']).exists()
        self.assertFalse(user_exist)
