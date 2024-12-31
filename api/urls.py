from django.urls import path, include
from .views import home, movie_search

urlpatterns = [
    path('', home, name='home'),
    path('search-movie/', movie_search.as_view(), name='search-movie')
]

