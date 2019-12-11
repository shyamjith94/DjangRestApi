from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from recipe import serializers
from rest_framework.test import APIClient
from rest_framework import status
from core.models import (
    Recipe,
    Tag,
    Ingredients)

RECIPE_URL = reverse('recipe:recipe-list')


def sample_tag(user, name='main course'):
    """To Create Return Tag With User"""
    return Tag.objects.create(user=user, name=name)


def sample_ingredients(user, name='main ingredients'):
    """Create And Return Ingredients"""
    return Ingredients.objects.create(user=user, name=name)


def sample_recipe(user, **params):
    """create And Return Recipe"""
    default = {
        'title': 'my_title',
        'time_minute': '10',
        'price': '5.00',
        }
    default.update(params)
    return Recipe.objects.create(user=user, **default)


def detail_url(recipe_id):
    """To Create Detail Url"""
    # In Detail View Need To Pass Recipe Id,Create Here
    return reverse('recipe:recipe-detail', args=[recipe_id])


class PublicRecipeApiTest(TestCase):
    """Test Public Recipe Api, UnAuthenticated Access To Api"""

    def setUp(self):
        self.client = APIClient()

    def test_required_auth(self):
        """Authentication Is Required"""
        res = self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    """Test For Private Recipe APi"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            'test7@gmail.com',
            'test@123'
            )
        self.client.force_authenticate(self.user)

    def test_retrieve_recipes(self):
        """Test For Retrieve Recipes"""
        sample_recipe(user=self.user)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.all().order_by('-id')
        serializer = serializers.RecipeSerializers(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_limited_user(self):
        """Recipes Are Limited To Authenticated User"""
        user2 = get_user_model().object.create_user(
            email='Test9@gmail.com',
            password='test5@123'
            )
        sample_recipe(user=user2)
        sample_recipe(user=self.user)
        res = self.client.get(RECIPE_URL)
        recipes = Recipe.objects.filter(user=self.user)
        serializer = serializers.RecipeSerializers(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_recipe_detail_view(self):
        """Test For Recipe Detail View"""
        recipe = sample_recipe(user=self.user)
        # adding recipe model foreign key fields
        recipe.tag.add(sample_tag(user=self.user))
        recipe.ingredients.add(sample_ingredients(user=self.user))
        # generating url
        url = detail_url(recipe.id)
        res = self.client.get(url)
        serializer = serializers.RecipeDetailSerializer(recipe)
        self.assertEqual(res.data, serializer.data)
