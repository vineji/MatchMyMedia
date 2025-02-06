import requests
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from suprise import SVD, Dataset, Reader
from suprise.model_selection import train_test_split

import os
from dotenv import load_dotenv

load_dotenv()


nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_books_from_google_api(query):
    
        api_key = os.getenv("TMBD_API_KEY")

        recommendations = []

        start_index = 0

        excluded_categories = ['Cooking','Self-Help','Health & Fitness','Hobbies','Crafts',
                               'Gardening','Travel','Art','Photography']
        

        try:

            while len(recommendations) < max_results:

                url = "https://www.googleapis.com/books/v1/volumes"
                query_string = f"{query['title']} {' '.join(query['keywords'])} {query['genre']}"

                param_list = {
                     "q" : query_string,
                     "maxResults" : 40,
                     "startIndex" : start_index,
                     "key" : api_key
                }

                response = requests.get(url, params=param_list)
                response.raise_for_status()

                books_data = response.json()

                for book in books_data.get("items", []):
                    volumeInfo = book.get("volumeInfo", {})
                    categories = volumeInfo.get("categories", [])

                    if not categories or any(category in excluded_categories for category in categories):
                        continue
                
                    recommendations.append({
                        "title" : volumeInfo.get("title", "Unknown Title"),
                        "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                        "description" : volumeInfo.get("description", "No Description Available"),
                        "categories" : categories,
                        "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
                    })
                
                start_index += len(books_data.get("items", []))
                if len(books_data.get("items", [])) < 40:
                     break
            return recommendations[:40]
        
        except Exception as e:
            print(f"Error fetching books: {e}")
            return []
        
                


