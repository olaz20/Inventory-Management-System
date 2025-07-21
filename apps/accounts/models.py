from django.db import models
from common.models import Audit
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser, Audit):
    """
    Custom user model that extends Django's AbstractUser.
    This model can be extended with additional fields as needed.
    """
    pass

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"