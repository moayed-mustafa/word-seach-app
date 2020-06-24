



from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


# create models
    # user model
class User(db.Model):
    """  create the user table in the database """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    image_url = db.Column(db.String, default='https://images.unsplash.com/photo-1543109740-4bdb38fda756?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80')
    gender = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable =False)