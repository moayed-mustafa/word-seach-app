"""
    Testing the routes that has to do with user login and signup

"""

# run these tests like:
# make sure you are in test directory
#    python -m unittest test_auth_routes.py



import os
from unittest import TestCase

# from models import db, User
from user.user_model import db, connect_db, Word,User

from sqlalchemy.exc import IntegrityError


os.environ['DATABASE_URL'] = "postgresql:///word-search-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class UserAuthTestCase(TestCase):
    """ testing the auth routes to check:
             can log in user.
             can log out user.
             can signup user.
             renders correctly.
             redirects correctly.
     """
# ===================================================================================================

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

    def test_login_route_no_user(self):
        with self.client as client:
            # check user not logged in:
            res = client.get('/login')
            self.assertEqual(res.status_code, 200)
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || Login</title>'
            self.assertIn(tag, html)

# ===================================================================================================

    def test_login_route_with_user(self):
        with self.client as client:
             # test with user logged in
            res = client.post('/login',data={"username": self.user.username, "password": self.user.password})
            self.assertEqual(res.status_code, 200)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || Login</title>'
            self.assertIn(tag, html)
# ===================================================================================================
    def test_signup(self):
        with self.client as client:
             # test with user logged in
            res = client.post('/login',data={"username": self.user.username, "password": self.user.password})
            self.assertEqual(res.status_code, 200)
            with client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.user.id
            html = res.get_data(as_text=True)
            tag = '<title>Word Search || Login</title>'
            self.assertIn(tag, html)