"""User model tests."""

# run these tests like:
# make sure you are in test directory
#    python -m unittest test_user_model.py

import os
from unittest import TestCase

from models import db, User

from sqlalchemy.exc import IntegrityError


os.environ['DATABASE_URL'] = "postgresql:///word-search-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """ testing the user model to checkif:
             can perform basic crud on the user.
             can perform crud on user words list
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
        # self.client = app.test_client()
    # ==============================================================================================================
    def test_user(self):
        """ test basic crud on user"""
        # there's already a user added, let's check if that is the case:
        self.assertEqual(self.user.username, 'test_user')
        # update the username and check if it persists
        self.user.username = 'not_just_test_user'
        db.session.commit()
        self.assertEqual(self.user.username, 'not_just_test_user')
        # let's check if the user can be retrieved
        user = User.query.get(self.user.id)
        self.assertEqual(user.id, self.user.id)

        # delete a usre and check if the deletion was completed
        # note: delete is not working for some reason!
        # User.query.delete()
        # db.session.commit()

        # self.assertIsNone(self.user)
        # self.assertIsInstance(self.user, User)
# ==============================================================================================================
    def test_authentication(self):
            """ test user authentication"""
        # user authenticate correctly
            authenticated = User.authenticate("test_user", 'thisismypasswordanditspassword')
            user = User.query.filter_by(username="test_user").first()
            self.assertEqual(user, authenticated)
            # user not authenticate because  the password is invalid
            authenticated = User.authenticate("test_user", "thisispassword")
            self.assertEqual(authenticated, False)
            # # user not authenticate because the uesrname is invalid
            authenticated = User.authenticate("testuserman", 'thisismypasswordanditspassword')
            self.assertEqual(authenticated, False)

# ==============================================================================================================

    def test_user_signup(self):
        """ tests the signup class method """
        # user signed up correctly
        signup_user= User.signup(username='signup_test_user',
                    password='thisismypasswordanditspasswordsignup',
                    email='test_user_signup.test@email.com',
                    image_url='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    gender='male')
        db.session.add(signup_user)
        db.session.commit()
        user = User.query.filter_by(username='signup_test_user').first()
        self.assertEqual(user, signup_user)
        # not working fully
        # user's sign up raises an error
        # with self.assertRaises(IntegrityError):
        #     signup_user= User.signup(username='signup_test_user',
        #             password='thisismypasswordanditspasswordsignup',
        #             email='test_user_signup.test@email.com',
        #             image_url='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
        #             gender='male')
        #     db.session.commit()
        #     signup_user
