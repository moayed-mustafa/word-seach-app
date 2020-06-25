


""" seed some data into the database """
from models import User, db, connect_db
from app import app

db.drop_all()
db.create_all()

# create a user
user = User.signup('testuser', 'testuserpassword','user.user@email.com', 'https://images.unsplash.com/photo-1586529726010-2411a6bec3c8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80' ,'male')
db.session.add(user)
db.session.commit()
