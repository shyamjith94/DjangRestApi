from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag, Recipe
from recipe import serializers

TAGS_URL = reverse('recipe:tag-list')


class PublicApiTagTests(TestCase):
    """Test The Tag Publicly Available"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test Login Required For Tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status
                         .HTTP_401_UNAUTHORIZED)


class PrivateApiTagTests(TestCase):
    """Test Authorized User Tags"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().object.create_user(
            email='test@gmail.com',
            password='test_pass@123')
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test Tat Retrieve Tags"""
        Tag.objects.create(user=self.user, name='test1')
        Tag.objects.create(user=self.user, name='test2')
        res = self.client.get(TAGS_URL)
        tag = Tag.objects.all().order_by('-name')
        serializer = serializers.TagSerializer(tag, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tag_limited_user(self):
        """Test The Tags Are Returned For Authenticated User"""
        user2 = get_user_model().object.create_user(
            email='othertest@gmail.com',
            password='test_other@123')
        Tag.objects.create(user=user2, name='other')
        tag = Tag.objects.create(user=self.user, name='test user')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test Create Tag Successful"""
        payload = {'name': 'test tag'}
        self.client.post(TAGS_URL, payload)
        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
            ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating new Invalid Payload"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_tags_assigned_to_recipes(self):
        """Test filtering tags by those assigned to recipes"""
        tag1 = Tag.objects.create(user=self.user, name='Breakfast')
        tag2 = Tag.objects.create(user=self.user, name='Lunch')
        recipe = Recipe.objects.create(
            title='Coriander eggs on toast',
            time_minute=10,
            price=5.00,
            user=self.user,
            )
        recipe.tag.add(tag1)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        serializer1 = serializers.TagSerializer(tag1)
        serializer2 = serializers.TagSerializer(tag2)
        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_tags_assigned_unique(self):
        """Test filtering tags by assigned returns unique items"""
        tag = Tag.objects.create(user=self.user, name='Breakfast')
        recipe1 = Recipe.objects.create(
            title='Pancakes',
            time_minute=5,
            price=3.00,
            user=self.user
            )
        recipe1.tag.add(tag)
        recipe2 = Recipe.objects.create(
            title='Porridge',
            time_minute=3,
            price=2.00,
            user=self.user
            )
        recipe2.tag.add(tag)

        res = self.client.get(TAGS_URL, {'assigned_only': 1})

        self.assertEqual(len(res.data), 1)
