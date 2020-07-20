"""
    Testing the  api routes created to support ajax requests

"""





import os
from unittest import TestCase

# from models import db, User, Word
from user.user_model import db, Word,User

from sqlalchemy.exc import IntegrityError


os.environ['DATABASE_URL'] = "postgresql:///word-search-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class TestApi(TestCase):

# ===================================================================================================

    def setUp(self):
        """ create a user to use for testing """
        User.query.delete()
        Word.query.delete()
        self.user = User.signup(username='test_user',
                    password='thisismypasswordanditspassword',
                    email='test_user.test@email.com',
                    image_url='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    gender='male')
        db.session.add(self.user)


        # make a testword:
        self.word = Word(word='blue', definition="of the color intermediate between green and violet; having a color similar to that of a clear unclouded sky",
        part_of_speech='adjective', synonym="blueish", example="October's bright blue weather")
        db.session.add(self.word)
        self.user.words.append(self.word)

        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()
# ===================================================================================================
    def test_add_word(self):
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            # in the info, you want to send, definition, partOfSpeech, examples as an array, synonyms as an array
            info = {'definition': 'provide housing for', 'example': ['The immigrants were housed in a new development outside the town'],
                    'partOfSpeech': 'verb',  'synonyms':['domiciliate']}

            url = '/add-word'
            res = client.post(url, json={'word': 'house', 'pronunciation': 'haʊs', 'info': info } )
            data = res.json
            self.assertEqual(res.status_code, 201)
            self.assertEqual(res.json, None)
# ===================================================================================================
    def test_delete_word(self):
        definition = self.word.definition
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id

            url = '/delete-word'
            res = client.post(url, json={'definition': definition})
            # Assert
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.data , b'Word Removed!')

            # word does not exist
            res = client.post(url, json={'definition': 'a game played with a ball and a net'})
            self.assertEqual(res.status_code, 202)



# ===================================================================================================
    def test_find_user(self):
        # with user
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            url = '/user-exists'
            res = client.get(url)
            # Assert
            self.assertEqual(res.status_code, 200)
# ===================================================================================================
    def test_find_guest(self):
        # without user
        with self.client as client:

            url = '/user-exists'
            res = client.get(url)
            # Assert
            self.assertEqual(res.status_code, 202)
# ===================================================================================================
    def test_find_word_in_user_list(self):
        # with user
        definition = self.word.definition
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            url = '/find-word'
            data={'definition': definition}
            res = client.post(url, json=data)
            # Assert
            # print(res)
            self.assertEqual(res.status_code, 200)