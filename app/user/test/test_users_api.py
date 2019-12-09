from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# url should constant
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


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

    def test_create_token_user(self):
        """Test That Token Created For User"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Token Not Created Invalid Credentials Are Given"""
        create_user(email="test@gmail.com", password='test_pass@123')
        payload = {
            'email': 'test@gmail.com',
            'password': 'wrong'
            }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """"Test Tht Token Not Created If user Doesn't Exist"""
        payload = {
            'email': 'test@gmail.com',
            'password': 'test_pass@123'
            }
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test Tht Email And Password Are Required"""
        res = self.client.post(TOKEN_URL,
                               {
                                   'email': 'one',
                                   'password': ''
                                   }
                               )
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)