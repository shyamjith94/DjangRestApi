from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_sample_user(
        email='test@gmail.com',
        password='test_passs@123'
        ):
    """Test That Create New Sample User"""
    return get_user_model().object.create_user(email, password)


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
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    """Test Tag"""

    def test_tag_str(self):
        """Test The Tag string representation"""
        tag = models.Tag.objects.create(
            user=create_sample_user(),
            name='Vegan'
            )
        self.assertEqual(str(tag), tag.name)

    def test_ingredients(self):
        """Test The Ingredients string representation"""
        ingredients = models.Ingredients.objects.create(
            user=create_sample_user(),
            name='Test Ingredients'
            )
        self.assertEqual(str(ingredients), ingredients.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=create_sample_user(),
            title='Steak and mushroom sauce',
            time_minute=5,
            price=5.00
            )

        self.assertEqual(str(recipe), recipe.title)
