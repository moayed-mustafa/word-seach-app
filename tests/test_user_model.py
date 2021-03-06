"""User model tests."""



import os
from unittest import TestCase

# from models import db, User
from user.user_model import db, Word,User

from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc


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
        self.user = User.signup('the_test_user',
                    'thisismypasswordanditspassword',
                    'test_user.test@email.com',
                    'https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    'male')
        db.session.add(self.user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()
    # ==============================================================================================================
    def test_user(self):
        """ test basic crud on user"""
        # there's already a user added, let's check if that is the case:
        self.assertEqual(self.user.username, 'the_test_user')
        # update the username and check if it persists
        self.user.username = 'not_just_test_user'
        db.session.commit()
        self.assertEqual(self.user.username, 'not_just_test_user')
        # let's check if the user can be retrieved
        user = User.query.get(self.user.id)
        self.assertEqual(user.id, self.user.id)


# ==============================================================================================================
    def test_authentication(self):
            """ test user authentication"""
        # user authenticate correctly
            authenticated = User.authenticate("the_test_user", 'thisismypasswordanditspassword')
            user = User.query.filter_by(username="the_test_user").first()
            self.assertEqual(user, authenticated)
            # user not authenticate because  the password is invalid
            authenticated = User.authenticate("test_user", "thisispassword")
            self.assertEqual(authenticated, False)
            # # user not authenticate because the uesrname is invalid
            authenticated = User.authenticate("testuserman", 'thisismypasswordanditspassword')
            self.assertEqual(authenticated, False)

# ==============================================================================================================

    def test_user_signup_valid(self):
        """ tests the signup class method """
        # user signed up correctly
        signup_user_test= User.signup('signup_user',
                    'thisismypasswordanditspasswordsignup',
                    'signup.test@email.com',
                    'https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    'male')
        db.session.add(signup_user_test)
        db.session.commit()
        user_test = User.query.filter_by(username='signup_user').first()
        self.assertIsNotNone(user_test)
        self.assertEqual(user_test.username, 'signup_user')
        self.assertEqual(user_test.email, 'signup.test@email.com')
        self.assertNotEqual(user_test.password, 'thisismypasswordanditspasswordsignup')
        # bcrypt should start with $2b$
        self.assertTrue(user_test.password.startswith('$2b$'))

# ==============================================================================================================
    def test_user_signup_invalid(self):
        user = User.signup('user',
                    'password',
                    'test_user_signup.test@email.com',
                    'https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    'male')
        db.session.add(user)
        db.session.commit()
        invalid = User.signup('user',
                    'password',
                    'test_user_signup.test@email.com',
                    'https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80',
                    'male')

        with self.assertRaises(exc.IntegrityError) as context:
            db.session.add(invalid)
            db.session.commit()

# ==============================================================================================================
