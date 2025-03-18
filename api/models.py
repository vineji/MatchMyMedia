from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import JSONField
import json

# Create your models here.


class Genre(models.Model):

    name = models.CharField(max_length=30, unique=True)
    colour = models.CharField(max_length=255, unique=False, default='#41ceaa')

    def __str__(self):
        return self.name
    
class User(AbstractUser):

    online_id = models.CharField(max_length=255, unique=True)
    favourite_genres = models.ManyToManyField(Genre, blank=True)
    favourite_books= models.JSONField(default=list, blank=True)
    DOB = models.DateField(null=True,blank=True)

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

    def get_genres(self):
        return [[x.name,x.colour] for x in self.favourite_genres.all()]
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username': self.username,
            'online_id': self.online_id,
            'DOB': self.DOB,
            'favourite_genres': self.get_genres(),
            'favourite_books': self.favourite_books

        }
    

class BookRating(models.Model):
    user_id = models.IntegerField(default=0)
    book_id = models.CharField(max_length=255)
    rating = models.FloatField()

    def __str__(self):
        return f"{self.user_id} - {self.book_id} - {self.rating}"
