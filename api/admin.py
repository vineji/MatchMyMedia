from django.contrib import admin
from .models import Genre, User, BookRating, FriendRequest, Friendship, SharedBooks

# Register your models here.
admin.site.register(User)
admin.site.register(Genre)
admin.site.register(BookRating)
admin.site.register(FriendRequest)
admin.site.register(Friendship)
admin.site.register(SharedBooks)

