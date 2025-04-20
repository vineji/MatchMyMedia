from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import FriendRequest, Friendship, Genre, BookRating
import json
from unittest.mock import patch
import uuid

# Create your tests here.

class BaseClass(TestCase):

    @classmethod
    def setUpClass(cls):
        # Called before the first test in each class
        super().setUpClass()
        cls.test_results = {} # Stores test results
    
    def setUp(self):
        # Called before each test in the class

        User = get_user_model()

        # Creates a test user
        self.test_user = User.objects.create_user(
            username = 'testUser',
            password = 'testPassword123',
            DOB = '2004-08-10',
            online_id = 'testOnlineID'
        )

        # Adding a favourite genre to the test user
        self.horror_genre = Genre.objects.filter(name='Horror').first()
        self.test_user.favourite_genres.add(self.horror_genre)

        self.client = Client() # Django test client for sending requests (mock browser)
    
    @classmethod
    def tearDownClass(cls):
        # Called after the last test in the class
        super().tearDownClass()

        # Prints all the test names and results
        class_name = cls.__name__.replace('Tests', '')
        print(f"\n---------- {class_name} Test Results ------------")
        for test_name, test_result in cls.test_results.items():
            print(f"Test: {test_name} ----- Result: {test_result}")
        print(f"------------------------------------------------\n")
    
    def tearDown(self):
        # Called after each test in the class
        
        test_name = self._testMethodName

        if not hasattr(self, '_outcome'):
            return
        
        result = self._outcome.result

        # Finds the result of the test

        # Checks for failed test assertions
        if len(result.failures) > 0 and result.failures[-1][0].id() == self.id():
            self.__class__.test_results[test_name] = "Test Failed"
        # Checks for errors
        elif len(result.errors) > 0 and result.errors[-1][0].id() == self.id():
            self.__class__.test_results[test_name] = "Test Error"
        # If there is no failure or error that the test has passed
        else:
            self.__class__.test_results[test_name] = "Test Passed"

class AuthenticationTests(BaseClass):

    def test_1_successful_login(self):
        try:
            # Valid username and password from setUp
            login_data = {
                'username' : 'testUser',
                'password' : 'testPassword123'
            }

            # Send POST request to login endpoint
            response = self.client.post('/login/', login_data)

            # 302 = redirection and the page url should be for dashboard page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/dashboard/')
            
            # Sends a request to the user_view which is protected by @login_required
            user_response = self.client.get('/user/')
            self.assertEqual(user_response.status_code, 200) # Should return 200 to verify user session

            user_data = json.loads(user_response.content) # Loads fetched user data

            # Check if the fetched user data is same as the test user data that was used to login
            self.assertEqual(user_data['username'], 'testUser')
            self.assertEqual(user_data['online_id'], 'testOnlineID')

            print("Test 1 ---- Successful login test passed")

        except Exception as e:
            print(f"Test error: {str(e)}")
            raise e # Raises the error
    
    def test_2_failed_login(self):
        try:
            # Invalid username and password
            login_data = {
                'username' : 'testUser',
                'password' : 'wrongPassword'
            }
            
            # Send POST request to login endpoint
            response = self.client.post('/login/', login_data)

            # No redirection (remains in login page)
            self.assertEqual(response.status_code, 200)
            self.assertIn('error', response.context) # Return true if error message exists

            # Sends a request to the user_view which is protected by @login_required
            user_response = self.client.get('/user/')
            self.assertNotEqual(user_response.status_code, 200) # Should not return 200 to verify unauthenticated user request

            print("Test 2 ---- Failed login test passed")
        
        except Exception as e:
            print(f"Test error: {str(e)}")
            raise e # Raises the error
    
    def test_3_successful_signup(self):

        try:

            signup_data = {
                'username' : 'UnIqU3uS3R',
                'password1' : 'uniquePassword123',
                'password2' : 'uniquePassword123',
                'online_id' : 'UnIqU3uS3R_ID',
                'DOB' : '2001-03-02'
            }
            # Send POST request to signup endpoint
            response = self.client.post('/signup/', signup_data)

            if response.status_code == 200:
                # Checks if response has context attribute
                if hasattr(response, 'context') and response.context != None:
                    form = response.context.form
                    # Prints any errors with the form
                    if form != None:
                        print(f"Form errors: {form.errors}")
                # Prints any other error
                if response.context.error:
                    print(f"Message: {response.context.error}")
            
            # 302 = redirection and the page url should be for dashboard page
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.url, '/dashboard/')

            User = get_user_model()
            # Retrieves the created user by filtering with the unique username
            created_user = User.objects.filter(username = signup_data["username"]).first()
            self.assertIsNotNone(created_user) # Return true if the object is not None which means user was created

            # Sends a request to the user_view which is protected by @login_required
            user_response = self.client.get('/user/')
            self.assertEqual(user_response.status_code, 200) # Should return 200 to verify user session

            user_data = json.loads(user_response.content) # Loads fetched user data

            # Check if the fetched user data is same as the test user data that was used to signup
            self.assertEqual(user_data['username'], signup_data['username'])
            self.assertEqual(user_data['online_id'], signup_data['online_id'])

            print("Test 3 ---- Successful signup test passed")

        except Exception as e:
            print(f"Test error: {str(e)}")
            raise e # Raises the error
    
    def test_4_failed_signup(self):

        try:

            # signup data with different passwords
            signup_data = {
                'username' : 'failedUser',
                'password1' : 'uniquePassword123',
                'password2' : 'wrongPassword',
                'online_id' : 'failedUser_ID',
                'DOB' : '2002-06-02'
            }

            # Send POST request to signup endpoint
            response = self.client.post('/signup/', signup_data)

            # No redirection, should stay on signup page
            self.assertEqual(response.status_code, 200)
            self.assertIn('error', response.context)

            User = get_user_model()

            not_created_user = User.objects.filter(username = signup_data["username"]).first()
            self.assertIsNone(not_created_user)

            print("Test 4 ---- Failed signup test passed")
        
        except Exception as e:
            print(f"Test error: {str(e)}")
            raise e # Raises the error

class RecommendationTests(BaseClass):

    def test_1_fetch_book_recommendation(self):

        try:

            # Meta data on movie, Harry Potter and the Goblet of Fire
            data = {
                'title' : 'Harry Potter and the Goblet of Fire',
                'description' : "When Harry Potter's name emerges from the Goblet of Fire, he becomes a competitor in a grueling battle for glory among three wizarding schools—the Triwizard Tournament.",
                'genre' : ['Fantasy', 'Adventure'],
                'type' : 'Movie'
            }

            # Send GET request to recommendation endpoint
            response = self.client.get('/get-recommendations/', data)

            # Should return 200 status code
            self.assertEqual(response.status_code, 200)
            response_data = json.loads(response.content)

            # Store book recommendations
            recommendations = response_data.get('recommendations', [])

            self.assertTrue(len(recommendations) > 0) # If length > 0 then it return recommendations

            print(f"Received {len(recommendations)} book recommendations")
            if recommendations != []:
                top_book = recommendations[0] # Print top recommended book
                print(f"Top recommendation: {top_book['title']} by {', '.join(top_book['authors'])}")
            
            print("Test 1 ---- Get book recommendations test passed")
        
        except Exception as e:
            print(f"Test error: {str(e)}")
            raise e # Raises the error


class UserFeaturesTests(BaseClass):
    
    # Called before each test in UserFeaturesTests
    def setUp(self):
        super().setUp() # For every test in this class the user is required to be logged in
        self.client.login(username='testUser', password='testPassword123')
    
    def test_1_add_existing_genre_to_favourites(self):

        fantasy_genre, _ = Genre.objects.get_or_create(name='Fantasy')

        data = {
            'action' : 'add_genre',
            'genre_name' : 'Fantasy'
        }

        response = self.client.post(
            '/user/',
            json.dumps(data), # API endpoint expects JSON so dumps converts from dict to json
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        test_user = User.objects.get(username='testUser')
        self.assertIn(fantasy_genre, test_user.favourite_genres.all())

        print("Test 1 ---- Favourite existing genre passed")

    def test_2_create_new_genre(self):
        # Testing for creating a new genre
        data = {
            'genre_name' : 'uNiQU3_G3nRE' # uniques genre name to avoid duplicate genres
        }

        response = self.client.post(
            '/genre/',
            json.dumps(data), # API endpoint expects JSON so dumps converts from dict to json
            content_type = 'application/json'
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Genre.objects.filter(name=data['genre_name']).exists()) # Return true if the genre is in the genre table

        print("Test 2 ---- Create new genre test passed")
    
    def test_3_add_and_rate_favourite_book(self):
        # Testing for favouriting and rating a book

        test_book = {
            'id' : 'test_book_id',
            'title' : 'TEST BOOK',
            'authors' : 'Test Author',
            'published_date' : '2002-09-02',
            'description' : 'This is the test book',
            'categories' : ['Testing'],
            'image' : 'http://test_example.com/image.png'
        }

        data = {
            'action' : 'add_book',
            'book' : test_book
        } 

        # Send POST request to user endpoint
        response = self.client.post(
            '/user/',
            json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

        # Check is book is in test user's favourites
        User = get_user_model()
        test_user = User.objects.get(username='testUser')
        result1 = self.assertIn(test_book, test_user.favourite_books)

        rating_data = {
            'book_id' : test_book['id'],
            'book_rating' : 4
        }

        # Send POST request to book rating endpoint
        rating_response = self.client.post(
            '/book-rating/',
            json.dumps(rating_data),
            content_type='application/json'
        )

        self.assertEqual(rating_response.status_code, 200)

        test_book_rating = BookRating.objects.get(
            user=self.test_user,
            book_id=test_book['id'] # Get the book rating by filtering using the test user and test_book id
        )

        self.assertEqual(test_book_rating.rating, 4)  # Checks if it has the same rating

        print("Test 3 ---- Add book to favourite and rate book test passed")
    

    def test_4_send_and_accept_friend_request(self):
        # Testing for sending and accepting friend request

        User = get_user_model()
        friend = User.objects.create_user( # Created another user to send a friend request to
            username='acceptUser',
            password='acceptPassword',
            online_id='acceptUser_id',
            DOB = '2001-03-11',
        )

        data = {'friend_id' : friend.id}
        
        # Sending a post request to using friend request endpoint
        response = self.client.post( 
            '/friend-request/',
            json.dumps(data),
            content_type='application/json'
        )


        self.assertEqual(response.status_code, 200)

        friend_request = FriendRequest.objects.get(from_user=self.test_user, to_user=friend)

        self.assertEqual(friend_request.status, 'pending') # Checks if the created friend request is pending

        self.client.force_login(friend) # Logging in as the other user to accept friend request

        accept_data = {
            'action' : 'accept',
            'request_id' : friend_request.id
        }
        # Sending a put request to using friend request endpoint
        accept_response = self.client.put(
            '/friend-request/',
            json.dumps(accept_data),
            content_type='application/json'
        )

        self.assertEqual(accept_response.status_code, 200)

        friend_request.refresh_from_db() # Gets updated friend request after accepting
        self.assertEqual(friend_request.status, 'accepted') # Checks if status is accepted


        # When a friend request is accepted two friendship instances are created
        friendship_created1 = Friendship.objects.filter(from_user=self.test_user, to_user=friend)
        friendship_created2 = Friendship.objects.filter(from_user=friend, to_user=self.test_user)

        # Checks if both friendship instances exist
        self.assertTrue(friendship_created1)
        self.assertTrue(friendship_created2)

        print("Test 4 ---- Send and accept friend request test passed")
    

    def test_5_send_and_decline_friend_request(self):
        # Testing for sending and declining friend request

        User = get_user_model()
        friend = User.objects.create_user( # Created another user to send a friend request to
            username='declineUser',
            password='declinePassword',
            online_id='declineUser_id',
            DOB = '2001-08-12',
        )

        data = {'friend_id' : friend.id}
        
        # Sending a post request to using friend request endpoint
        response = self.client.post( 
            '/friend-request/',
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)

        friend_request = FriendRequest.objects.get(from_user=self.test_user, to_user=friend)

        self.assertEqual(friend_request.status, 'pending') # Checks if the created friend request is pending

        self.client.force_login(friend) # Logging in as the other user to decline friend request

        decline_data = {
            'action' : 'decline',
            'request_id' : friend_request.id
        }
        # Sending a put request to using friend request endpoint
        decline_response = self.client.put(
            '/friend-request/',
            json.dumps(decline_data),
            content_type='application/json'
        )

        self.assertEqual(decline_response.status_code, 200)

        friend_request.refresh_from_db() # Gets updated friend request after declining

        self.assertEqual(friend_request.status, 'declined') # Checks if the status is now declined

        # When a friend request is accepted two friendship instances are created so we need to make sure they have not been created when declined
        friendship_created1 = Friendship.objects.filter(from_user=self.test_user, to_user=friend)
        friendship_created2 = Friendship.objects.filter(from_user=friend, to_user=self.test_user)

        # Checks if both friendship instances do not exist
        self.assertFalse(friendship_created1)
        self.assertFalse(friendship_created2)

        print("Test 5 ---- Send and decline friend request test passed")
    

    def test_6_share_and_unshare_book_with_friend(self):
        # Testing for sharing and unsharing books between friends

        User = get_user_model()
        friend = User.objects.create_user( 
            username='shareUser',
            password='sharePassword',
            online_id='shareUser_id',
            DOB = '1998-08-12',
        )
        
        # Books shared from test_user to friend will be stored in this instance
        Friendship.objects.create(from_user=self.test_user, to_user=friend)

        # Books shared from friend to test_user will be stored in this instance
        Friendship.objects.create(from_user=friend, to_user=self.test_user)

        share_book = { # Book that will be shared
            'id' : 'share_book_id',
            'title' : 'SHARE BOOK',
            'authors' : 'Share Author',
            'published_date' : '2003-09-02',
            'description' : 'This is the shared book',
            'categories' : ['Sharing'],
            'image' : 'http://test_example.com/image.png'
        }

        data = {
            'to_user_id' : friend.id,
            'book' : share_book
        }

        # Request to share book from test_user to friend via share books endpoint
        share_response = self.client.post(
            '/share-book/',
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(share_response.status_code, 200)

        friendship = Friendship.objects.get(from_user=self.test_user, to_user=friend)

        # Checks if the book is in shared_books
        self.assertTrue(any(book.get('id') == share_book['id'] for book in friendship.shared_books))

        # Request to unshare book from test_user to friend via share books endpoint
        unshare_response = self.client.delete(
            '/share-book/',
            json.dumps(data),
            content_type='application/json'
        )

        self.assertEqual(unshare_response.status_code, 200)

        friendship.refresh_from_db() # Gets updated friendship object after unsharing book

        # Checks if the book is not in shared_books
        self.assertFalse(any(book.get('id') == share_book['id'] for book in friendship.shared_books))

        print("Test 6 ---- Share and unshare book with friend test passed")
    

    def test_7_cannot_share_book_with_non_friend(self):
        # Testing for restrictions with sharing between non-friends

        User = get_user_model()
        non_friend = User.objects.create_user( 
            username='nonFriendUser',
            password='nonFriendPassword',
            online_id='nonFriendUser_id',
            DOB = '1996-08-12',
        )

        # Deletes any existing friendships between test_user and non_friend if there is any
        Friendship.objects.filter(from_user=self.test_user, to_user=non_friend).delete()
        Friendship.objects.filter(from_user=non_friend, to_user=self.test_user).delete()

        share_book = { # Book that will be attempted to be shared
            'id' : 'share_book_id',
            'title' : 'SHARE BOOK',
            'authors' : 'Share Author',
            'published_date' : '2003-09-02',
            'description' : 'This is the shared book',
            'categories' : ['Sharing'],
            'image' : 'http://test_example.com/image.png'
        }

        data = {
            'to_user_id' : non_friend.id,
            'book' : share_book
        }

        # Send POST request to share book endpoint
        response = self.client.post(
            '/share-book/',
            json.dumps(data),
            content_type='application/json'
        )

        response_data = response.json()

        # Chceks for 400 error statud code and error message
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response_data)

        print("Test 7 ---- Cannot share book with non-friend test passed")















        







        

    

    



    



    

        







            
            










            



