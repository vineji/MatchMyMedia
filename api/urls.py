from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path("home", views.main_spa),
    path('', views.main_spa, name='main page'),
    path('login/', views.login_view, name='login page'),
    path('signup/', views.sign_up_view, name='signup page'),
    path('search-movie/', views.movie_search_view, name='search-movie'),
    path('search-show/', views.show_search_view, name='search-show'),
    path('search-book/', views.book_search_view, name='search-book'),
    path('get-recommendations/', views.get_book_recommendations_view, name='get-recommendations')


]

