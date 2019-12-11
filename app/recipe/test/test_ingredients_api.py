from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Ingredients
from recipe.serializers import IngredientsSerializer

INGREDIENTS_URL = reverse('recipe:ingredients-list')


class PublicIngredientsTest(TestCase):
    """Test Public Ingredients Api"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test LoginRequired For Access Api"""
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientsTest(TestCase):
    """Test Private Ingredients Api"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'ingredients@gmail.com',
            'ingredients@123'
            )
        self.client.force_authenticate(self.user)

    def test_listing_ingredients(self):
        """Test Listening Ingredients List"""
        Ingredients.objects.create(user=self.user, name='my_test1')
        Ingredients.objects.create(user=self.user, name='my_test2')
        res = self.client.get(INGREDIENTS_URL)
        ingredients = Ingredients.objects.all().order_by('-name')
        serializer = IngredientsSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_for_authenticated_user(self):
        """Test That Ingredients Model Limited To Authenticated User"""
        user = get_user_model().object.create_user(
            'test5@gmail.com',
            'test@pass123'
            )
        Ingredients.objects.create(user=user, name='check123')
        # assign to variable to creation for check its matches
        ingredients = Ingredients.objects.create(user=self.user, name='again')
        res = self.client.get(INGREDIENTS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredients.name)

    def test_create_ingredients_successful(self):
        """Test Create Ingredients Successfully"""
        payload = {
            'name': 'cabbage'
            }
        self.client.post(INGREDIENTS_URL, payload)
        exists = Ingredients.objects.filter(
            user=self.user,
            name=payload['name']
            ).exists()
        self.assertTrue(exists)

    def test_ingredients_invalid(self):
        """Test To Post Invalid Ingredients"""
        payload = {
            'name': ''
            }
        res = self.client.post(INGREDIENTS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

