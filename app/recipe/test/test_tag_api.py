from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
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
        user2 =get_user_model().object.create_user(
            email='othertest@gmail.com',
            password='test_other@123')
        Tag.objects.create(user=user2, name='other')
        tag = Tag.objects.create(user=self.user, name='test user')
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
