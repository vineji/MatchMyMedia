from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests


def main_spa(request):
    return render(request, 'index.html')

class movie_search(APIView):
    def get(self,request, format=None):

        title = request.GET.get('title','')

        if not title:
            return Response({'movies':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = '75c89f5935bea75e58f550b0d0476ad2'
        url = f'https://api.themoviedb.org/3/search/movie?query={title}&api_key={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            movies = data['results']
            return Response({'movies':movies})
        else:
            return Response({'movies':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class show_search(APIView):
    def get(self,request, format=None):

        title = request.GET.get('title','')
        page_number = request.GET.get('page',1)

        if not title:
            return Response({'shows':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = '75c89f5935bea75e58f550b0d0476ad2'
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