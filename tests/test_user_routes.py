"""
    Testing the routes that has to do with user blueprint

"""

# run these tests like:
# make sure you are in test directory
#    python -m unittest test_user_routes.py

import os
from unittest import TestCase

from models import db, User

from sqlalchemy.exc import IntegrityError


os.environ['DATABASE_URL'] = "postgresql:///word-search-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserRoutesTestCase(TestCase):
    """ testing the user routes to check:

    """
    def setUp(self):
        """ create a user to use for testing """
        User.query.delete()
        self.user = User.signup(username='test_user',
                    password='thisismypasswordanditspassword',
                    email='test_user.test@email.com',
                    image_url='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    gender='male')
        db.session.add(self.user)
        db.session.commit()
        self.client = app.test_client()
# ===================================================================================================
    def test_user_profile_update(self):
        """  test the update user route """
        with self.client as client:
            url = f'profile/{self.user.id}/user'
            res = client.get(url)
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.location, 'http://localhost/')
# ===================================================================================================
    def test_user_profile_update_post(self):
        """  test the update user route """
        with self.client as client:
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            url = f'profile/{self.user.id}/user'
            res = client.post(url)
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || Edit Profile</title>'
            self.assertIn(tag, html)
# ===================================================================================================
    def test_user_list(self):
        """  test the update user words list route """
        with self.client as client:
            url = f'/list/{self.user.id}/user'
            res = client.get(url)

            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || user list</title>'
            self.assertIn(tag, html)
# ===================================================================================================
    def test_user_search(self):
        """ tests the search page """
        with self.client as client:
            url = f'/search/{self.user.id}/user'
            res = client.get(url)

            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || search</title>'
            self.assertIn(tag, html)
# ===================================================================================================
