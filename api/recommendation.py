import requests
import spacy
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split

import os
from dotenv import load_dotenv

load_dotenv()


nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")


def fetch_books_from_google_api(query):
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    recommendations = []

    start_index = 0
    
    max_results = 40
    
    filtered_categories = ["fiction", "drama", "adventure", "fantasy", "horror", "action", "comedy", "history", "western"
                           , "crime", "mystery", "romance", "magic", "family", "war", "kids", "children", "sci-fi", "comic", "novel", "graphic"]

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

                if not categories or not any(any(fc in category.lower() for fc in filtered_categories) for category in categories):
                    continue
            
                recommendations.append({
                    "title" : volumeInfo.get("title", "Unknown Title"),
                    "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date" : volumeInfo.get("publishedDate", "Unknown"),
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


def extract_keywords(text, n=5):
    
    doc = nlp(text)
    words = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]

    vectorizer = TfidfVectorizer(stop_words='english')
    tfIdf_matrix = vectorizer.fit_transform([" ".join(words)])
    feature_arr = vectorizer.get_feature_names_out()
    tfIdf_sorting = tfIdf_matrix.toarray().flatten().argsort()[::-1]


    return [feature_arr[i] for i in tfIdf_sorting[:n]]

def rank_books_by_cosine_similarity(movie_query, books):
     
    movie_embedding = model.encode(movie_query["description"], convert_to_tensor=True)

    ranked_books = []

    for book in books:
        book_embedding = model.encode(book["description"], convert_to_tensor=True)
        similarity_score = util.pytorch_cos_sim(movie_embedding, book_embedding)
        ranked_books.append((book,similarity_score))
    
    ranked_books.sort(key=lambda x: x[1], reverse=True)
    return [book[0] for book in ranked_books]
    

def get_recommended_books(movie_query):

    movie_query["keywords"] = extract_keywords(movie_query["description"])

    books = fetch_books_from_google_api(movie_query)

    ranked_book_recommendations = rank_books_by_cosine_similarity(movie_query, books)

    return ranked_book_recommendations



                


