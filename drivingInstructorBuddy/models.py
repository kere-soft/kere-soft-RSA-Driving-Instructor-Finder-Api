from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    password = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    verification_code = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()


class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    recommendations = models.IntegerField(default=0, null=False, blank=False)
    about = models.CharField(max_length=512, null=True, blank=True)


class Learner(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    name = models.CharField(max_length=128, blank=False, null=False)
    avatar = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    county = models.CharField(max_length=128, null=True, blank=True)

