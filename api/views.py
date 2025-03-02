from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from . import recommendation

from rest_framework import status

import requests

import os
from dotenv import load_dotenv

load_dotenv()


def main_spa(request):
    return render(request, 'index.html')

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


