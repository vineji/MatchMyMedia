import requests
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split
from .models import BookRating
import os
from dotenv import load_dotenv
import hashlib
from django.core.cache import cache


import json

load_dotenv()




def fetch_books_from_google_api(query):

    # Fetches books from Google Books API using query parameters (title, genres and extracted keywords)
    
    api_key = os.getenv("GOOGLE_BOOKS_API_KEY")

    recommendations = []

    start_index = 0 # Will be incremented by 40 to fetch the next 40 books

    start_index_title = 0
    
    max_results = 40 # The API returns 40 results at a time

    # The API will return many unrelated books such as cooking books or manuals they will be filtered using the array below
    filtered_categories = ["fiction", "drama", "adventure", "fantasy", "horror", "action", "comedy", "western"
                           , "crime", "mystery", "romance", "magic", "war", "kids", "children", "sci-fi", "comic", "novel", "graphic"]

    try:

        while len(recommendations) < max_results: # Recommendation will contain a maximum of 40 books

            url = "https://www.googleapis.com/books/v1/volumes" # URL to fetch books

            # We are making two requests to the API
            
            query_string = f"{query['keywords']} {query['genre']}" # Contains keywords extracted from description and genres

            query_string_title = f"{query['title']}" # Contains only the title

            

            param_list = { # Params for fetching books using query string (keywords and genres)
                "q" : query_string,
                "maxResults" : 40,
                "startIndex" : start_index,
                "key" : api_key
            }

            # Some movies and shows are based on actual books so we are going to fetch only using title.
            # Only upto 5 results as some books that are returned can be completely unrelated to the show or movie.

            param_list_title = { # Params for fetching books using title query string
                "q" : query_string_title,
                "maxResults" : 5,
                "startIndex" : start_index_title,
                "key" : api_key
            }

            response_title = requests.get(url, params=param_list_title) # Sends request to API with params containing title only
            response_title.raise_for_status() # Checks is request was successful or not
            books_title_data = response_title.json() # Converts from json to python dictionary

            # appends every filtered book in specific dictionary format to recommendations
            for book in books_title_data.get("items", []):
                volumeInfo = book.get("volumeInfo", {}) # This is where all the meta information of each book is stored
                categories = volumeInfo.get("categories", [])

                # Converts retrieved category (genre) and converts to lowercase and checks if it is in filtered_categories
                if not categories or not any(any(fc in category.lower() for fc in filtered_categories) for category in categories):
                    continue
            
                recommendations.append({
                    "id" : book.get("id"),
                    "title" : volumeInfo.get("title", "Unknown Title"),
                    "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date" : volumeInfo.get("publishedDate", "Unknown"),
                    "description" : volumeInfo.get("description", "No Description Available"),
                    "categories" : categories,
                    "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
                })

            response = requests.get(url, params=param_list) # Sends same request as above but with the params with extracted keywords and genres only
            response.raise_for_status()
            books_data = response.json()

            for book in books_data.get("items", []):
                volumeInfo = book.get("volumeInfo", {})
                categories = volumeInfo.get("categories", [])

                if not categories or not any(any(fc in category.lower() for fc in filtered_categories) for category in categories):
                    continue
            
                recommendations.append({
                    "id" : book.get("id"),
                    "title" : volumeInfo.get("title", "Unknown Title"),
                    "authors" : volumeInfo.get("authors", ["Unknown Author"]),
                    "published_date" : volumeInfo.get("publishedDate", "Unknown"),
                    "description" : volumeInfo.get("description", "No Description Available"),
                    "categories" : categories,
                    "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
                })
            
            start_index += 40 # Increments to the next 40 books
            start_index_title += 5 # Increments to the next 5 books

            # This if statement ensures that even if there is less than 40 recommendations it should come out the loop (max iterations is 4)
            # This ensures that the user is not waiting too long for recommendations
            if start_index > 121: 
                break
        
        dupe_title_date = set() # A set to store unique tuples (title, published_date)
        final_recommendations = []

        for book in recommendations: # If the tuple is not in the set then the book is added to final recommendations and tuple is added to the set
            # If it is in set then it is duplicate book and will not be added to final recommendations
            if (book["title"],book["published_date"]) not in dupe_title_date:
                final_recommendations.append(book)
                dupe_title_date.add((book["title"],book["published_date"]))
            
        return final_recommendations
    
    except Exception as e:
        print(f"Error fetching books: {e}")
        return []


def extract_keywords(text, n=5):

    # Measure the importantance of each word and converting to TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english',max_features=n)
    tfIdf_matrix = vectorizer.fit_transform([text])
    # Gets the features (words) from the matrix
    feature_arr = vectorizer.get_feature_names_out()
    # Converts the matrix (2D array) into 1D and sorts it in descending order
    tfIdf_sorting = tfIdf_matrix.toarray().flatten().argsort()[::-1]

    return [feature_arr[i] for i in tfIdf_sorting[:n]]


def fetch_books_from_google_api_using_id(id):
    # This method return specific books by using the API to search using the book id
    # Every book in the API has an ID

    # This method is for getting the meta info of books from the collaborative filtering method
        
    url = f"https://www.googleapis.com/books/v1/volumes/{id}"

    response = requests.get(url)

    response.raise_for_status()
    book_data = response.json()
    
    volumeInfo = book_data.get("volumeInfo", {})
    categories = volumeInfo.get("categories", [])


    # In some returned descriptions that contain HTML tags so this is used to filter them out
    phrases_to_remove = ["<p>","</p>","<br>","</br>","<b>","</b>","<i>","</i>"]

    description = volumeInfo.get("description", "No Description Available")

    for x in phrases_to_remove:
        description = description.replace(x, "")

    return {
        "id" : book_data.get("id"),
        "title" : volumeInfo.get("title", "Unknown Title"),
        "authors" : volumeInfo.get("authors", ["Unknown Author"]),
        "published_date" : volumeInfo.get("publishedDate", "Unknown"),
        "description" : description,
        "categories" : categories[:3],
        "image" : volumeInfo.get("imageLinks", {}).get("thumbnail")
    }


def get_collaborative_filtering_recommendations():

    user_ratings = BookRating.objects.all()

    if not user_ratings:
        return []
    
    print(user_ratings)

    reader = Reader(rating_scale=(1,5))

    data = Dataset.load_from_df(
        pd.DataFrame(list(user_ratings.values("user__id", "book_id", "rating"))),
        reader
    )

    train_set, test_set = train_test_split(data, test_size=0.2)

    model = SVD()
    model.fit(train_set)

    predictions = model.test(test_set)

    book_predictions = {}

    for uid, iid, true_r, est, _ in predictions:
        if iid not in book_predictions:
            book_predictions[iid] = est
        else:
            book_predictions[iid] += est
    
    
    recommended_books = sorted(book_predictions.items(), key=lambda x : x[1], reverse=True)


    top_recommended_books= [fetch_books_from_google_api_using_id(book[0]) for book in recommended_books[:10]]

    return top_recommended_books


def rank_books_by_cosine_similarity(media_query, books):

    media_query_description = media_query.get("description", "")

    book_descriptions = [book.get("description", "") for book in books]

    vectorizer = TfidfVectorizer(stop_words="english")
    # Learns vocabulary from all the books and media query descriptions
    vectorizer.fit(book_descriptions + [media_query_description])

    media_query_vector = vectorizer.transform([media_query_description])

    book_vectors = vectorizer.transform(book_descriptions)

    cos_similarity_scores = cosine_similarity(media_query_vector, book_vectors).flatten()

    ranked_books = sorted(zip(books, cos_similarity_scores), key=lambda x : x[1], reverse=True)

    return [book[0] for book in ranked_books][:27]


def get_recommended_books(media_query):

    cache_title = media_query.get('title', '').lower().strip()
    cache_genres = media_query.get('genre', '').lower().strip()

    cache_string = f"{cache_title}-{cache_genres}"
    hashed_key = hashlib.md5(cache_string.encode()).hexdigest()
    cache_key = f"recommendation_key_{hashed_key}"

    cached_recommendations = cache.get(cache_key)

    if cached_recommendations:
        return cached_recommendations
    


    media_query["keywords"] = extract_keywords(media_query["description"])

    books = fetch_books_from_google_api(media_query)

    books += get_collaborative_filtering_recommendations()

    ranked_book_recommendations = rank_books_by_cosine_similarity(media_query, books)

    cache.set(cache_key, ranked_book_recommendations, timeout=900)

    return ranked_book_recommendations



                


