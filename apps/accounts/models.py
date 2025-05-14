from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager as UserManager

# Create your models here.

class CustomUser(AbstractUser):
    TYPE = (
        ('organizer', 'Organizer'),
        ('participant', 'Participant'),
        ('admin', 'Admin'),
    )
    username = None
    role = models.CharField(max_length=20, choices=TYPE, default='participant')
    email = models.EmailField(unique=True)
    
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()

    def __str__(self):
        return self.email


