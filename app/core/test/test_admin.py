from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().object.create_superuser(
            email='test@gmail.com',
            password="test@_pass123"
            )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().object.create_user(
            # Same Email Address Will Give Integrity Error Email Fields are Unique
            email='tes2t@gmail.com',
            password='test_pass123',
            name='Test User Full Name',
            )

    def test_users_listed(self):
        """Test are Users Listed In user Page"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

