from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.conf import settings

import uuid
import os
from django.utils.translation import gettext as _


def recipe_image_file_path(instance, filename):
    """Using For Generate New FIle Path"""
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('uploads/recipe/', filename)


# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address!')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model that supports using email instead of username"""
    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    object = UserManager()

    def __str__(self):
        return self.email


class Tag(models.Model):
    """Tag To Used For Recipe"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    """Ingredients Model"""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Recipe Model"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    title = models.CharField(max_length=255)
    time_minute = models.IntegerField()
    price = models.FloatField()
    link = models.CharField(max_length=255, blank=True)
    ingredients = models.ManyToManyField('Ingredients')
    tag = models.ManyToManyField('Tag')
    image_field = models.ImageField(null=True, upload_to=recipe_image_file_path)

    def __str__(self):
        return self.title
