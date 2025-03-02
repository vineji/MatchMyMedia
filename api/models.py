from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.

class Genre(models.Model):

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    online_id = models.CharField(max_length=255, unique=True)
    favourite_genres = models.ManyToManyField(Genre, blank=True)
    favourite_books= models.JSONField(default=list, blank=True)

    groups = models.ManyToManyField(
        Group,
        related_name = "custom_user_set",
        blank = True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name = "custom_user_permissions_set",
        blank = True
    )




