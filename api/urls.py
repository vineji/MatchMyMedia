from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_spa, name='main page'),
    path('search-movie/', views.movie_search.as_view(), name='search-movie'),
    path('search-show/', views.show_search.as_view(), name='search-show'),
    path('search-book/', views.book_search.as_view(), name='search-book'),
    path('get-recommendations/', views.get_book_recommendations.as_view(), name='get-recommendations')


]

