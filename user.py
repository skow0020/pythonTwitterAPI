from database import CursorFromConnectionFromPool
import oauth2
from twitter_utils import consumer
import json


class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oath_token = oauth_token
        self.oath_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):
        return "<User {}>".format(self.screen_name)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES (%s, %s, %s)',
                            (self.screen_name, self.oath_token, self.oath_token_secret))

    @classmethod
    def load_from_db_by_screen_name(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE screen_name=%s', (screen_name,))
            user_data = cursor.fetchone()
            if user_data:
                return cls(user_data[1], user_data[2], user_data[3], user_data[0])

    def twitter_request(self, uri, verb='GET'):
        # Create an authenticated_token' object and use it to perform twitter API calls on behalf of the user
        authorized_token = oauth2.Token(self.oath_token, self.oath_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)

        # make twitter api calls!
        response, content = authorized_client.request(uri, verb)
        if response.status != 200:
            print("Error occurred getting the image")

        return json.loads(content.decode('utf-8'))

