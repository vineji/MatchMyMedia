from django.urls import path, include
from .views import movie_search, show_search

urlpatterns = [
    path('search-movie/', movie_search.as_view(), name='search-movie'),
    path('search-show/', show_search.as_view(), name='search-show')
]

