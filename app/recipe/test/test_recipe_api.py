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

# image uploading
import tempfile
import os
from PIL import Image

RECIPE_URL = reverse('recipe:recipe-list')


def image_upload_url(recipe_id):
    """Generate For Image Upload Url Return It"""
    return reverse('recipe:recipe-upload-image', args=[recipe_id])


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
            'tag': [tag1.id, tag2.id],
            'time_minute': 30,
            'price': 10.00
            }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        tags = recipe.tag.all()
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
            'time_minute': 45,
            'price': 15.00
            }
        res = self.client.post(RECIPE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        recipe = Recipe.objects.get(id=res.data['id'])
        ingredients = recipe.ingredients.all()
        self.assertEqual(ingredients.count(), 2)
        self.assertIn(ingredient1, ingredients)
        self.assertIn(ingredient2, ingredients)

    def test_recipe_partial_update(self):
        """Test For Partial Update Recipe Model"""
        recipe = sample_recipe(user=self.user)
        recipe.tag.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='new tag')
        payload = {
            'title': 'chicken',
            'tag': [new_tag.id]
            }
        url = detail_url(recipe.id)
        self.client.patch(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        tag = recipe.tag.all()
        self.assertEqual(len(tag), 1)
        self.assertIn(new_tag, tag)

    def test_recipe_full_fields_update(self):
        """Test Full Fields Update Recipes Model"""
        recipe = sample_recipe(user=self.user)
        recipe.tag.add(sample_tag(user=self.user))
        payload = {
            'title': 'special title',
            'time_minute': 10,
            'price': 12.0
            }
        url = detail_url(recipe.id)
        self.client.put(url, payload)
        recipe.refresh_from_db()
        self.assertEqual(recipe.title, payload['title'])
        self.assertEqual(recipe.time_minute, payload['time_minute'])
        self.assertEqual(recipe.price, payload['price'])
        tag = recipe.tag.all()
        self.assertEqual(len(tag), 0)


class RecipeImagUpload(TestCase):
    """Tests For Image Uploads"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            email='image@gmail.com',
            password='image@123')
        self.client.force_authenticate(self.user)
        self.recipe = sample_recipe(user=self.user)

    def tearDown(self):
        """Run After The Test Function"""
        self.recipe.image.delete()

    def test_upload_image_to_recipe(self):
        """Test uploading an image to recipe"""
        url = image_upload_url(self.recipe.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as ntf:
            img = Image.new('RGB', (10, 10))
            img.save(ntf, format='JPEG')
            ntf.seek(0)
            res = self.client.post(url, {'image': ntf}, format='multipart')

        self.recipe.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('image', res.data)
        self.assertTrue(os.path.exists(self.recipe.image.path))

    def test_filter_recipes_by_tags(self):
        """Test returning recipes with specific tags"""
        recipe1 = sample_recipe(user=self.user, title='Thai vegetable curry')
        recipe2 = sample_recipe(user=self.user, title='Aubergine with tahini')
        tag1 = sample_tag(user=self.user, name='Vegan')
        tag2 = sample_tag(user=self.user, name='Vegetarian')
        recipe1.tag.add(tag1)
        recipe2.tag.add(tag2)
        recipe3 = sample_recipe(user=self.user, title='Fish and chips')

        res = self.client.get(
            RECIPE_URL,
            {'tag': '{},{}'.format(tag1.id, tag2.id)}
            )

        serializer1 = serializers.RecipeSerializers(recipe1)
        serializer2 = serializers.RecipeSerializers(recipe2)
        serializer3 = serializers.RecipeSerializers(recipe3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)

    def test_filter_recipes_by_ingredients(self):
        """Test returning recipes with specific ingredients"""
        recipe1 = sample_recipe(user=self.user, title='Posh beans on toast')
        recipe2 = sample_recipe(user=self.user, title='Chicken cacciatore')
        ingredient1 = sample_ingredients(user=self.user, name='Feta cheese')
        ingredient2 = sample_ingredients(user=self.user, name='Chicken')
        recipe1.ingredients.add(ingredient1)
        recipe2.ingredients.add(ingredient2)
        recipe3 = sample_recipe(user=self.user, title='Steak and mushrooms')

        res = self.client.get(
            RECIPE_URL,
            {'ingredients': '{},{}'.format(ingredient1.id, ingredient2.id)}
            )

        serializer1 = serializers.RecipeSerializers(recipe1)
        serializer2 = serializers.RecipeSerializers(recipe2)
        serializer3 = serializers.RecipeSerializers(recipe3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
