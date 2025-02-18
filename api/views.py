from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from . import recommendation
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

import os
from dotenv import load_dotenv

load_dotenv()


def main_spa(request):
    return render(request, 'index.html')

class movie_search(APIView):
    def get(self,request, format=None):

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)

        if not title:
            return Response({'movies':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = os.getenv("TMBD_API_KEY")
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
            return Response(response_data)
        else:
            return Response({'movies':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class show_search(APIView):
    def get(self,request, format=None):

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)

        if not title:
            return Response({'shows':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = os.getenv("TMBD_API_KEY")
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
            return Response(response_data)
        else:
            return Response({'shows':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class book_search(APIView):
    def get(self,request,format=None):

        title = request.GET.get('title', '')
        page_number = request.GET.get('page', 1)
        startIndex = 10 * (int(page_number) - 1)
        maxItemsPerPage = 20

        if not title:
            return Response({'items':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = os.getenv("GOOGLE_BOOKS_API_KEY")
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
            return Response(response_data)
        else:
            return Response({'books':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class get_book_recommendations(APIView):
    def get(self,request,format=None):

        data = request.GET.dict()

        recommendations = recommendation.get_recommended_books(data) 

        return JsonResponse({"recommendations": recommendations})


