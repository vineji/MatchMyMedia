from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import requests

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
            movies = data['results'][:30]
            return Response({'movies':movies})
        else:
            return Response({'movies':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class show_search(APIView):
    def get(self,request, format=None):

        title = request.GET.get('title','')

        if not title:
            return Response({'shows':[]}, status=status.HTTP_400_BAD_REQUEST)
        
        api_key = '75c89f5935bea75e58f550b0d0476ad2'
        url = f'https://api.themoviedb.org/3/search/tv?query={title}&api_key={api_key}'

        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            tv_shows = data['results'][:30]
            return Response({'shows':tv_shows})
        else:
            return Response({'shows':[]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)