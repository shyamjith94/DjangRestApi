from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from core.models import Ingredients, Recipe
from rest_framework.test import APIClient
from core.models import Ingredients
from recipe.serializers import (
    IngredientsSerializer,
    TagSerializer,
    RecipeSerializers)

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

    def test_retrieve_ingredients_assigned_to_recipes(self):
        """Test filtering ingredients by those assigned to recipes"""
        ingredient1 = Ingredients.objects.create(
            user=self.user, name='Apples'
            )
        ingredient2 = Ingredients.objects.create(
            user=self.user, name='Turkey'
            )
        recipe = Recipe.objects.create(
            title='Apple crumble',
            time_minute=5,
            price=10.00,
            user=self.user
            )
        recipe.ingredients.add(ingredient1)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        serializer1 = IngredientsSerializer(ingredient1)
        serializer2 = IngredientsSerializer(ingredient2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_ingredient_assigned_unique(self):
        """Test filtering ingredients by assigned returns unique items"""
        ingredient = Ingredients.objects.create(user=self.user, name='Eggs')
        recipe1 = Recipe.objects.create(
            title='Eggs benedict',
            time_minute=30,
            price=12.00,
            user=self.user
            )
        recipe1.ingredients.add(ingredient)
        recipe2 = Recipe.objects.create(
            title='Green eggs on toast',
            time_minute=20,
            price=5.00,
            user=self.user
            )
        recipe2.ingredients.add(ingredient)

        res = self.client.get(INGREDIENTS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)


