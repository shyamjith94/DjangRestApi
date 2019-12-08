from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test Create new with email successful"""
        email = "test@gmail.com"
        password = "test_pass123"
        user = get_user_model().object.create_user(
            email=email,
            password=password
            )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test to New User Email Is Normalized"""
        email = "test@GMAIL.COM"
        user = get_user_model().object.create_user(email, 'test_pass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Create New User With Out Email Raise Value Error"""
        with self.assertRaises(ValueError):
            get_user_model().object.create_user(None, 'test_pass123')

    def test_create_new_superuser(self):
        """Test For Creating New Supper User"""
        email = 'test@gmail.com'
        password = 'test_pass123'
        user = get_user_model().object.create_superuser(email, password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

