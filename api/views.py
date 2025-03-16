from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from . import recommendation
import json
from rest_framework import status

import requests

import os
from dotenv import load_dotenv

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, get_user_model, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token

from .forms import CustomUserCreationForm, CustomUserUpdateForm

from .models import Genre

load_dotenv()


def main_spa(request):
    return render(request, 'index.html')

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})

def login_view(request):
    if request.method== "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print(request.session.items())
            return redirect("http://127.0.0.1:8080/dashboard/")
        else:
            return render(request, "login.html", {"form": form, "error": "Invalid username or password."})
    form = AuthenticationForm()
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return render(request, "login.html")

def sign_up_view(request):
    if request.method== "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            login(request, user)
            return redirect("http://127.0.0.1:8080/dashboard/")
        else:
            print(form.errors)
            return render(request, "signup.html", {"form": form})
    
    form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

@login_required
def user_view(request):

    if request.method == "GET":
        if request.user.is_authenticated:
            user_data = request.user.to_dict()
            return JsonResponse(user_data)
        
    elif request.method == "PUT":

        data = json.loads(request.body)
        action = data.get('action')


        if not action:

            try:
                User = request.user

                updated_data = {
                    "username": data.get("username", User.username),
                    "online_id": data.get("online_id", User.online_id),
                    "email": data.get("email", User.email),
                    "DOB": data.get("DOB", User.DOB)
                }
                form  = CustomUserUpdateForm(updated_data, instance=request.user)
                if form.is_valid():
                    form.save()
                    return JsonResponse({"message": "User details updated successfully!"})
                else:
                    print(form.errors)
                    return JsonResponse({"errors": form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data."}, status=400)
    
    elif request.method == "POST":

        data = json.loads(request.body)
        action = data.get('action')
        
        if action == 'change_password':
            try:
                form = PasswordChangeForm(user=request.user, data = data)

                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    return JsonResponse({"message": "Password updated successfully!"})
                else:
                    print(form.errors)
                    return JsonResponse({"errors": form.errors}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON data."}, status=400)
        
        elif action == 'add_genre':

            try:
                genre_name = data.get('genre_name')

                if not genre_name:
                    return JsonResponse({"error": "Genre name is required"}, status=400)
                
                genre = Genre.objects.get(name=genre_name)

                request.user.favourite_genres.add(genre)
                request.user.save()

                return JsonResponse({"message": "Genre added successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        
        elif action == 'add_book':

            try:
                book = data.get('book')

                if not book:
                    return JsonResponse({"error": "Book is required"}, status=400)
                
                if book in request.user.favourite_books:
                    return JsonResponse({"error": "Book is already added to favourites"}, status=400)

                request.user.favourite_books.append(book)
                request.user.save()

                return JsonResponse({"message": "Book added successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
    
    elif request.method == 'DELETE':

        data = json.loads(request.body)
        action = data.get('action')

        
        if action == 'delete_genre':

            try:
                genre_name = data.get('genre_name')

                if not genre_name:
                    return JsonResponse({"error": "Genre name is required"}, status=400)
                
                genre = Genre.objects.get(name=genre_name)

                request.user.favourite_genres.remove(genre)
                request.user.save()

                return JsonResponse({"message": "Genre removed successfully."}, status=200)
            
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
                
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)


    print("user not authenticated")
    return JsonResponse({"error": "Invalid request method"}, status=405)

@login_required
def genre_view(request):

    if request.method == "GET":

        all_genres = Genre.objects.all()
        genre_list = [[genre.name,genre.colour] for genre in all_genres]

        return JsonResponse(genre_list, safe=False)
    
    elif request.method == "POST":
        try:

            data = json.loads(request.body)
            genre_name = data.get('genre_name')

            if not genre_name:
                return JsonResponse({"error": "Genre name is required"}, status=400)
            
            genre_name_cleaned = genre_name.strip().lower()

            genre = Genre.objects.filter(name__iexact=genre_name_cleaned).first()


            if genre:
                return JsonResponse({"message": "Genre already exists.","genre_name": genre.name,}, status=201)
            
            genre = Genre.objects.create(name=genre_name)

            return JsonResponse({
                "message": "Genre added to the database successfully.",
                "genre_name": genre.name,
            }, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)





def movie_search_view(request):
    
    if request.method == 'GET':

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)
        api_key = os.getenv("TMBD_API_KEY")

        if not title:
            url = f'https://api.themoviedb.org/3/trending/movie/day?api_key={api_key}&page={page_number}'
        else:
            url = f'https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}&page={page_number}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data['results']
            total_pages = data['total_pages']
            current_page = data['page']
            response_data = {
                'movies': movies,
                'total_pages': total_pages,
                'current_page': current_page,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'movies':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
def show_search_view(request):
        
    if request.method == 'GET':

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)
        api_key = os.getenv("TMBD_API_KEY")

        if not title:
            url = f'https://api.themoviedb.org/3/trending/tv/day?api_key={api_key}&page={page_number}'
        else: 
            url = f'https://api.themoviedb.org/3/search/tv?query={title}&api_key={api_key}&page={page_number}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            tv_shows = data['results']
            total_pages = data['total_pages']
            current_page = data['page']
            response_data = {
                'shows': tv_shows,
                'total_pages': total_pages,
                'current_page': current_page,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'shows':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

def book_search_view(request):
        
    if request.method == 'GET':

        title = request.GET.get('title', '')
        page_number = request.GET.get('page', 1)
        startIndex = 10 * (int(page_number) - 1)
        maxItemsPerPage = 20

        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

        if not title:
            url = f'https://www.googleapis.com/books/v1/volumes?q=subject:fiction&orderBy=Relevance&startIndex={startIndex}&maxResults={maxItemsPerPage}&key={api_key}'
        else:
            url = f'https://www.googleapis.com/books/v1/volumes?q={title}&startIndex={startIndex}&maxResults={maxItemsPerPage}&key={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            books = data['items']
            total_pages = data['totalItems'] // maxItemsPerPage
            current_page = page_number

            response_data = {
                'books': books,
                'total_pages': total_pages,
                'current_page': current_page
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({'books':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_book_recommendations_view(request):
        
    if request.method == 'GET':
        data = request.GET.dict()

        recommendations = recommendation.get_recommended_books(data) 

        return JsonResponse({"recommendations": recommendations})


