



import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from auth.auth import auth_BP
from general.general import general_BP
from user.user import user_BP

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
# if you want to check if your configurations is set, print(app.config)

# register your blueprints here
app.register_blueprint(auth_BP)
app.register_blueprint(general_BP)
app.register_blueprint(user_BP)

@app.route('/')
def test_app():
    return 'hello'