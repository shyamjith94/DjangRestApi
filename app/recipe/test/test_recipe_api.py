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

    def test_create_basic_recipe(self):
        """Test creating recipe"""
        payload = {
            'title': 'Test recipe',
            'time_minute': 30,
            'price': 10.00,
            }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(recipe, key))

    def test_create_recipe_with_tags(self):
        """Test creating a recipe with tags"""
        tag1 = sample_tag(user=self.user, name='Tag 1')
        tag2 = sample_tag(user=self.user, name='Tag 2')
        payload = {
            'title': 'Test recipe with two tags',
            'tags': [tag1.id, tag2.id],
            'time_minutes': 30,
            'price': 10.00
            }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_recipe_with_ingredients(self):
        """Test creating recipe with ingredients"""
        ingredient1 = sample_ingredients(user=self.user, name='Ingredient 1')
        ingredient2 = sample_ingredients(user=self.user, name='Ingredient 2')
        payload = {
            'title': 'Test recipe with ingredients',
            'ingredients': [ingredient1.id, ingredient2.id],
            'time_minutes': 45,
            'price': 15.00
            }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)
