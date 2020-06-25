



from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)


# create models
    # user model
class User(db.Model):
    __tablename__ = 'users'

    """  create the user table in the database """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String, default='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80')
    gender = db.Column(db.String, nullable=False)

    # add a sign up and authenticate methods:
    @classmethod
    def signup(cls, username, password, email, image_url, gender):
        """ hash password and create a user instance"""
        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8');
        user = User(username=username, password=hashed_password, email=email, image_url=image_url, gender=gender)

        return user



    @classmethod
    def authenticate(cls, username, password):
        """  takes form data that represents user credintials and verify the user identity """
        user = cls.query.filter_by(username=username).first()
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False







