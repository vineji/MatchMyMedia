from django.urls import path, include
from .views import home, MovieSearch_View

urlpatterns = [
    path('', home, name='home'),
    path('search-movie/', MovieSearch_View.as_view(), name='search-movie')
]

