from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager as UserManager

# Create your models here.


class CustomUser(AbstractUser):
    username = None
    is_organizer_pending = models.BooleanField(default=False)
    email = models.EmailField(unique=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
