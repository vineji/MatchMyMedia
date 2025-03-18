from django.contrib import admin
from .models import Genre, User, BookRating

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(BookRating)

