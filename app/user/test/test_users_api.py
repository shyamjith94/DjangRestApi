from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

# url should constant
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


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

    def test_retrieve_user_un_authorized(self):
        """Test That Authentication Required For User"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test Api Request Required Authentication"""

    def setUp(self):
        """Set Up Client To Variable"""
        self.user = create_user(
            email='test@gmail.com',
            password='test_pass@123',
            name='Test Name')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test Retrieve Profile Of Login User"""
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'name': self.user.name
            })

    def test_post_not_allowed(self):
        """Test For Reject POST Request"""
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test Update User Profile Authenticated User
           Update Using Refresh_From_Db Method
        """
        payload = {
            'name': 'New Name',
            'email': 'newemail@gmail.com',
            'password': 'newpassword@123'
            }
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
