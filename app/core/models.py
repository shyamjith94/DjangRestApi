from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Create your models here.

class UserManger(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create And Save New"""
        if not email:
            raise ValueError('User Must Have Email')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create And Save New Superuser"""
        user = self.create_user(email, password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model That Support Email of instead of Username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    object = UserManger()
    USERNAME_FIELD = 'email'
